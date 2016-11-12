import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import joinedload
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db)
import datetime
import spotipy

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ["APP_SECRET_KEY"]

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage"""

    return render_template("home.html")


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

    return render_template("festival_specific.html", festival_info=festival_info,
                                                     artist_list=artist_list)


@app.route('/preview.json', methods=['POST'])
def playlist_review():
    """Display static preview of songs on playlist."""

    playlist_artists = request.form.getlist("artists[]")
    print playlist_artists

    spotify = spotipy.Spotify()

    playlist_json = {}

    for artist in playlist_artists:
        artist_info = Artist.query.filter_by(artist_name=artist).first()
        artist_db_id = artist_info.artist_id
        artist_spot_id = artist_info.spotify_artist_id
        spotify_artist_uri = 'spotify:artist:' + artist_spot_id
        recently_updated = artist_info.top10_updated_at
        print artist_info.artist_name, "recently_updated", recently_updated
        today = datetime.datetime.today()
        print "today", today

        if recently_updated is None:

            new_top10_json = spotify.artist_top_tracks(spotify_artist_uri)
            new_top10_tracks = new_top10_json['tracks']

            for track in new_top10_tracks:
                track_name = track['name']
                track_id = track['id']

                new_song = Song(song_name=track_name,
                                artist_id=artist_db_id,
                                spotify_track_id=track_id)

                db.session.add(new_song)

            artist_info.top10_updated_at = today
            db.session.commit()

        elif recently_updated < (today - datetime.timedelta(days=7)):
            print "\n\n top10_updated_at has been updated!!!!!!"

            new_top10_json = spotify.artist_top_tracks(spotify_artist_uri)
            new_top10_tracks = new_top10_json['tracks']
            # new_top10_tracks.append({'name': 'haaaaay', 'id': 'NOT AN ID HAHAHAHAHA'})

            # current_db_songs = Song.query.filter_by(artist_id=artist_db_id).all()

            for track in new_top10_tracks:
                track_name = track['name']
                track_id = track['id']

                if not Song.query.filter_by(spotify_track_id=track_id).first():

                    new_song = Song(song_name=track_name,
                                    artist_id=artist_db_id,
                                    spotify_track_id=track_id)

                    db.session.add(new_song)

            artist_info.top10_updated_at = today
            db.session.commit()

        top_songs = Song.query.filter_by(artist_id=artist_db_id).all()
        print "\n\n", artist_info.artist_name, top_songs

        if len(top_songs) >= 3:
            random_songs = random.sample(top_songs, 3)
            print "\n\nrandom_songs:", random_songs

        else:
            random_songs = top_songs

        song_name_id = {}

        for song in random_songs:
            song_name_id[song.song_name] = song.spotify_track_id

        playlist_json[artist_info.artist_name] = song_name_id
        print "\n\nplaylist_json after adding", artist_info.artist_name, playlist_json

    print "\n\nfinal playlist_json:", playlist_json

    return jsonify(playlist_json)


@app.route('/generate')
def generate_playlist():
    """Create playlist and add songs to playlist."""

    pass


@app.route('/login', methods=['GET'])
def login_form():
    """Show form for login."""

    pass


@app.route('/login', methods=['POST'])
def login_process():
    """Process login form."""

    pass


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for registration."""

    pass


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration form."""

    pass


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
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")