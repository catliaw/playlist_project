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
    with open('seed_data/coachella_artists10.json') as json_data:
        d = json.load(json_data)

        for row in d:
            artist_name = row.get('artist')
            artist_url = row.get('website_url', None)
            artist_img = row.get('image_url', None)

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
    with open('seed_data/coachella_artists10.json') as json_data:
        d = json.load(json_data)

        stages = []

        for row in d:
            stage = row.get('stage', None).strip()

            if (stage not in stages) and (stage is not None):
                stages.append(stage)

                #Considering that Coachella is the only festival in db, index=1
                coachella_stage = Stage(stage_name=stage,
                                        festival_id=1)

                db.session.add(coachella_stage)

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
    with open('seed_data/coachella_artists10.json') as json_data:
        d = json.load(json_data)

        for row in d:
            # print row
            artist_name = row.get('artist')
            # print artist_name
            day1 = row.get('day1', None).strip()
            day2 = row.get('day2', None)
            stage = row.get('stage', None).strip()

            # Is this necessary if just Coachella?
            # festival_info = Festival.query.filter_by(festival_name="Coachella 2016").first()
            # fest_id = festival_info.festival_id

            artist_info = Artist.query.filter(Artist.artist_name.like(artist_name)).first()
            # print artist_info
            artist_id = artist_info.artist_id
            # print artist_id

            if day1 and (day1 is not None):
                day1_playing = datetime.strptime(day1, '%A, %B %d, %Y')
            else:
                day1_playing = None

            if day2 and (day2 is not None):
                day2 = day2.strip()
                day2_playing = datetime.strptime(day2, '%A, %B %d, %Y')
            else:
                day2_playing = None

            stage_info = Stage.query.filter_by(stage_name=stage).first()
            print stage_info
            stage_id = stage_info.stage_id

            festival_artist = FestivalArtist(festival_id=1,
                                             artist_id=artist_id,
                                             day1_playing=day1_playing,
                                             day2_playing=day2_playing,
                                             stage_id=stage_id)

            db.session.add(festival_artist)

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_festivals()
    load_coachella_artists()
    load_coachella_stages()
    load_festivalartists()
