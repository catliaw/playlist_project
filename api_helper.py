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
import spotipy.util as util
import os
import random


def find_spotify_userid(token):
    """Find user ID of user logged in."""

    spotify = spotipy.Spotify(auth=token)

    userid = spotify.current_user()['id']
    print "\n\nSpotify userid!", userid

    return userid
