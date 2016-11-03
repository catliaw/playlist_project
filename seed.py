from sqlalchemy import func
import json
from datetime import datetime
from server import app
from model import (Festival, FestivalArtist, Stage, Artist, Song, PlaylistSong,
    Playlist, User, connect_to_db, db)


def load_festivals():
    """Manually load Coachella festival information into database."""

    print "Festival Info"

    coachella = Festival(festival_name="Coachella 2016",
                         festival_url="https://www.coachella.com/")

    db.session.add(coachella)

    db.session.commit()


def load_coachella_artists():
    """Load artist info from coachella_artist10.json into database."""

    print "Coachella Artists"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate artists
    Artist.query.delete()

    # Read coachella_artist10.json file and insert artist data
    with open('seed_data/coachella_artist10.json') as json_data:
        d = json.load(json_data)

        for dict in d:
            artist_name = d.get('artist')
            artist_url = d.get('website_url', None)
            artist_img = d.get('image_url', None)

            artist = Artist(artist_name=artist_name,
                            artist_url=artist_url,
                            artist_img=artist_img)

            # We need to add to the session or it won't ever be stored
            db.session.add(artist)

        # Once we're done, we should commit our work
        db.session.commit()


def load_coachella_stages():
    """Load Coachella stage info."""

    print "Coachella Stages"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate stages
    Stage.query.delete()

    # Read coachella_artist10.json file and insert stage data
    with open('seed_data/coachella_artist10.json') as json_data:
        d = json.load(json_data)

        stages = []

        for dict in d:
            stage = d.get('stage', None)

            if (stage not in stages) and (stage is not None):
                stages.append(stage)

                #Considering that Coachella is the only festival in db, index=1
                coachella_stage = Stage(stage_name=stage,
                                        festival_id=1)

                db.session.add(artist)

            else:
                pass

        db.session.commit()


def load_festivalartists():
    """Load Coachella artist-festival-stage data into festival_artists relational table."""

    print "Coachella FestivalArtist"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate festival_artists rows
    FestivalArtist.query.delete()

    # Read coachella_artist10.json file and insert festival artist data
    with open('seed_data/coachella_artist10.json') as json_data:
        d = json.load(json_data)

        for dict in d:
            artist_name = d.get('artist')            
            day1 = d.get('day1', None).strip()
            day2 = d.get('day2', None).strip()
            stage = d.get('stage', None).strip()

            # Is this necessary if just Coachella?
            festival_info = Festival.query.filter_by(festival_name="Coachella 2016").first()
            festival_id = festival_info.festival_id

            artist_info = Artist.query.filter_by(artist_name = artist_name).first()
            artist_id = artist_info.artist_id

            if day1 and (day1 is not None):
                day1_playing = datetime.strptime(day1, '%A, %B %d, %Y')
            else:
                day1_playing = None

            if day2 and (day2 is not None):
                day2_playing = datetime.strptime(day2, '%A, %B %d, %Y')
            else:
                day2_playing = None

            artist_festival = ArtistFestival(festival_id=festival_id,
                                             artist_id=artist_id,
                                             day1_playing=day1_playing,
                                             day2_playing=day2_playing,
                                             stage=stage)

            db.session.add(artist)

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_festivals()
    load_coachella_artists()
    load_coachella_stages()
    load_festivalartists()
