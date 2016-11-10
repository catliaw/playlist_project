import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.orm import joinedload
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db)

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


@app.route('/preview', methods=['GET'])
def playlist_review():
    """Display static preview of songs on playlist."""

    artists = request.args.get("artists")

    print artists

    return artists


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