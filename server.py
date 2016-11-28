import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import joinedload
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db)
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import random
import api_helper
import helper_func
import pprint

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ["APP_SECRET_KEY"]

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Grabs app's Spotify client ID & secret from my secrets.sh file
spotify_client_id = os.environ['SPOTIPY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

# The Spotify scope authorization for the user
spotify_scope = 'playlist-modify-public'

# Initialize Spotify Client Credentials object with app's client ID/secret
client_credentials = SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret)

spotify_oauth = SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri=spotify_redirect_uri,
    state=None,
    scope=spotify_scope,
    cache_path=None)


@app.route('/')
def index():
    """Homepage"""

    spotify_authorize_url = spotify_oauth.get_authorize_url()
    url = spotify_authorize_url + '&show_dialog=true'

    return render_template("home.html", url=url)


@app.route('/festivals')
def festivals():
    """Page with links to festival specific pages."""

    festivals = Festival.query.order_by('festival_name').all()

    return render_template("festivals.html", festivals=festivals)


@app.route('/festivals/<festival_route>')
def specific_festival(festival_route):
    """Show festival specific form to select desired artist for playlist."""

    festival_info = Festival.query.filter_by(festival_route=festival_route).options(joinedload('festivalartists')).first()

    artist_list = festival_info.festivalartists

    artist_info = []

    helper_func.build_lineup_list(artist_list, artist_info)

    # print "\nFinal Artist Info List:", artist_info, "\n"
    # print "\nLength of Artist Info List:", len(artist_info), "\n\n"

    return render_template("festival_specific.html", festival_info=festival_info,
                                                     artist_info=artist_info,
                                                     length=len(artist_info))


@app.route('/preview.json', methods=['POST'])
def playlist_review():
    """Display static preview of songs on playlist."""

    playlist_json = {}

    playlist_artists = request.form.getlist("artists[]")
    # print playlist_artists

    # Get Spotify Client Credentials access token
    credential_token = client_credentials.get_access_token()
    # Initialize spotify as Spotipy object
    spotify = spotipy.Spotify(auth=credential_token)

    helper_func.parse_artist_to_playlist(playlist_json, playlist_artists, spotify)

    print "\n\nfinal playlist_json:", playlist_json, "\n"

    # {"artist1": {"song title 1": id1, "song title2": id2}, "artist2"}
    return jsonify(playlist_json)


@app.route('/generate', methods=['POST'])
def generate_playlist():
    """Connect to Spotify, create playlist, and add songs to playlist."""

    # List of track IDs from AJAX
    tracks_to_add = request.form.getlist("tracks[]")
    print "\n\n\nTracks to add:", tracks_to_add, "\n"

    # Check for valid access token, if not refresh access token
    token = api_helper.check_token_valid()

    # Spotify user ID from session
    user_spot_id = session['user_spot_id']

    # Need name of festival for name of playlist
    user_playlist_name = request.form.get("playlist_name")
    # print "\nUser Playlist Name:", user_playlist_name, "\n"

    playlist_name = helper_func.create_playlist_name(user_playlist_name)
    # print "\nFinal Playlist Name:", playlist_name, "\n"

    if token:
        print "\nToken valid!\n"

        spotify = spotipy.Spotify(auth=token)

        # Creating playlist
        playlist_info = api_helper.create_spotify_playlist(
            spotify, user_spot_id, playlist_name)
        # Adding tracks, function returns playlist_url
        playlist_url = api_helper.add_tracks(
            spotify, playlist_info, user_spot_id, tracks_to_add)

        url_info = {"url": playlist_url}

        return jsonify(url_info)

    else:
        print "\nCould not create playlist... :(\n"

        return redirect("/")


@app.route('/spotify_callback')
def callback():
    """Authorizes the user and gets token."""

    # Grade code from Spotify
    code = request.args.get('code')

    # Exchange code for token and store in session
    # Also find user's Spotify userid and store in session
    if code:
        api_helper.process_login(code)

        return redirect('/')

    # else redirect to homepage where can sign in.
    else:
        flash("Please login to Spotify!")

        return redirect('/')


@app.route('/logout')
def logout_process():
    """Processes logging out and clears session."""

    session.clear()
    print "\nSession was cleared!\n"

    flash("You have logged out!")

    return redirect('/')


@app.route('/account')
def account_info():
    """Display account information for user."""

    pass


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")