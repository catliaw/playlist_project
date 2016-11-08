"""Movie Ratings."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
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

    pass


@app.route('/festivals/<festival_route>')
def festival_route():
    """Festival specific page to select desired artist for playlist."""

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