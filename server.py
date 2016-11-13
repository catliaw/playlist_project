import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import joinedload
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db)
import datetime
import spotipy
import random

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
            #### (john) should move this into a separate function so you don't repeat this below
            #### design concern: might be beyond the scope of this project, but i would consider it
            #### good design to separate components that update the database vs ones that retrieve
            #### information. i.e. have a separate task or process that updates the database

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

        #### (john) a cleaner way to do this might be to do
        #### random.shuffle(top_songs)
        #### random_songs = top_songs[0:3]

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

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login form."""

    username = request.form.get('username')
    password = request.form.get('password')

    search_user = db.session.query(User)

    if search_user.filter_by(user_email=username, user_password=password).scalar() is not None:

        login_user_id = db.session.query(User.user_id).filter_by(user_email=username, password=password).scalar()

        session['login_user_id'] = login_user_id

        flash("Logged in.")

        return redirect(url_for('user_info', user_id=login_user_id))

    else:

        flash("Your password doesn't match our database!")

        return redirect('/')


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Processes register_form."""

    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')

    search_user = db.session.query(User)

    if search_user.filter_by(user_email=username).scalar() is None:

        new_user = User(user_email=username, user_fname=first_name, user_lname=last_name, user_password=password)

        db.session.add(new_user)

        db.session.commit()

        login_user_id = db.session.query(User.user_id).filter_by(user_email=username, user_password=password).scalar()

        session['login_user_id'] = login_user_id

        flash("Thank you for signing up! You are logged in.")

    # return redirect(url_for('user_info', user_id=login_user_id))
    return redirect("/")


@app.route('/logout')
def logout_process():
    """Processes logging out."""

    del session['login_user_id']

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
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")