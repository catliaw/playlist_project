import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import joinedload
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db, add_new_user)
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy.util as util
import os
import random

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

    refresh_token = token_info['refresh_token']
    session['refresh_token'] = refresh_token

    return token


def check_token_fresh():
    token = session['token']
    token_info = session['token_info']
    refresh_token = session['refresh_token']

    if not spotify_oauth._is_token_expired(token_info):
        spotify = spotipy.Spotify(auth=token)

    else:
        refresh_info = spotify_oauth._refresh_access_token(refresh_token)
        token_info = refresh_info[]




    return spotify


def find_spotify_userid(token):
    """Find user ID of user logged in."""

    spotify = spotipy.Spotify(auth=token)

    userid = spotify.current_user()['id']
    print "\n\nSpotify userid!", userid

    userid = api_helper.find_spotify_userid(spotify)

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
