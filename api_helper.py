import os
from flask import flash, session
from model import add_new_user
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import pprint

spotify_client_id = os.environ['SPOTIPY_CLIENT_ID']
spotify_client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
spotify_redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']

# The Spotify scope authorization for the user
spotify_scope = 'playlist-modify-public'

# Initialize Spotify Authentication object with app's client ID/secret
spotify_oauth = SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri=spotify_redirect_uri,
    state=None,
    scope=spotify_scope,
    cache_path=None)


def code_to_access_token(code):
    token_info = spotify_oauth.get_access_token(code)

    return token_info


def token_to_session(token_info):

    session['token_info'] = token_info

    token = token_info['access_token']
    session['token'] = token

    return token


def check_token_valid():
    token = session['token']
    token_info = session['token_info']

    if spotify_oauth._is_token_expired(token_info):
        refresh_token = spotify_oauth._refresh_access_token(token_info['refresh_token'])
        token = token_to_session(refresh_token)

    return token


def initialize_spotify():
    token = check_token_valid()

    if token:
        spotify = spotipy.Spotify(auth=token)
    else:
        print "\nSpotify Authentication token not valid!\n"

    return spotify


def find_spotify_userid(token):
    """Find user ID of user logged in."""

    spotify = spotipy.Spotify(auth=token)

    userid = spotify.current_user()['id']
    print "\n\nSpotify userid!", userid

    return userid


def add_userid_db_session(userid):
    """Take userid and add user to User table and session."""
    add_new_user(userid)

    session['user_spot_id'] = userid
    flash("Logged in.")


def process_login(code):
    """Log in user with Spotify OAuth."""

    token_info = code_to_access_token(code)
    token = token_to_session(token_info)
    userid = find_spotify_userid(token)
    add_userid_db_session(userid)


def create_spotify_playlist(spotify, userid, playlist_name):

    # Create playlist. Need user id, name of playlist, public (=True default)
    # spotify.user_playlist_create(user, name, public)
    playlist_info = spotify.user_playlist_create(
        user=userid,
        name=playlist_name,
        public=True)
    print "\nCreated playlist!\n"
    print "\nStart pretty printing playlist info\n"
    pprint.pprint(playlist_info)
    print "\nEnd pretty printing playlist info\n"

    return playlist_info


def add_tracks(spotify, playlist_info, userid, tracks_list):

    playlist_id = playlist_info['id']
    print "\nPlaylist Spotify ID", playlist_id, "\n"

    playlist_url = playlist_info['external_urls']['spotify']
    print "\nPlaylist URL", playlist_url, "\n"

    # ADD SONGS
    # spotify.user_playlist_add_tracks(
    #     user, playlist_id, tracks, position=None)
    print "\nAdding tracks into", playlist_info['name'], "\n"
    spotify.user_playlist_add_tracks(
        user=userid,
        playlist_id=playlist_id,
        tracks=tracks_list,
        position=None)

    return playlist_url


def spotify_top10(artist_uri, spotify):
    new_top10_json = spotify.artist_top_tracks(artist_uri)
    new_top10_tracks = new_top10_json['tracks']

    return new_top10_tracks


