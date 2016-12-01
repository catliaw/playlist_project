from sqlalchemy import func
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from datetime import datetime
from server import app
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db)


def load_more_festivals():
    """Manually load Coachella festival information into database."""

    print "Festival Info"

    coachella2015 = Festival(festival_name="Coachella 2015",
                             festival_route="coachella-2015",
                             festival_url="https://www.coachella.com/")

    snowglobe2016 = Festival(festival_name="Snowglobe 2016",
                             festival_route="snowglobe-2016",
                             festival_url="http://snowglobemusicfestival.com/")

    snowglobe2015 = Festival(festival_name="Snowglobe 2015",
                             festival_route="snowglobe-2015",
                             festival_url="http://snowglobemusicfestival.com/")

    lib2016 = Festival(festival_name="Life is Beautiful 2016",
                       festival_route="lifeisbeautiful-2016",
                       festival_url="http://lifeisbeautiful.com/")

    lib2015 = Festival(festival_name="Life is Beautiful 2015",
                       festival_route="lifeisbeautiful-2015",
                       festival_url="http://lifeisbeautiful.com/")

    osw2016 = Festival(festival_name="Outside Lands 2016",
                       festival_route="outsidelands-2016",
                       festival_url="http://www.sfoutsidelands.com/")

    osw2015 = Festival(festival_name="Outside Lands 2015",
                       festival_route="outsidelands-2015",
                       festival_url="http://www.sfoutsidelands.com/")

    db.session.add(coachella2015)
    db.session.add(snowglobe2016)
    db.session.add(snowglobe2015)
    db.session.add(lib2016)
    db.session.add(lib2015)
    db.session.add(osw2016)
    db.session.add(osw2015)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_festivals()
    # load_coachella_artists()
    # load_coachella_stages()
    # load_festivalartists()
