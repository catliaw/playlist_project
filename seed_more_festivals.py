from sqlalchemy import func
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from datetime import datetime
from server import app
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db)


def load_festivals():
    """Manually load Coachella festival information into database."""

    print "Festival Info"

    coachella = Festival(festival_name="Coachella 2016",
                         festival_route="coachella-2016",
                         festival_url="https://www.coachella.com/")

    db.session.add(coachella)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_festivals()
    # load_coachella_artists()
    # load_coachella_stages()
    # load_festivalartists()
