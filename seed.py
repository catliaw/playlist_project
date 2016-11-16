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


def load_coachella_artists():
    """Load artist info from coachella_artist10.json into database."""

    print "Coachella Artists"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate artists
    Artist.query.delete()

    artist_info_list = []

    # name_not_same = {}

    not_first_result = {
        "Bedouin": "5bKdC6382t97Qnpvs81Rqx",
        "DESPACIO": None,
        "Dirty Mop": "2L6ltv7c16hTJuAGZEVjrR",
        "DJ EZ": None,
        "Jesse Wright": None,
        "Lee K": None,
        "Lush": "3ysp8GwsheDcBxP9q65lBg",
        "NU": None,
        "Patricio": None,
        "Skin": "4rGWYVkJUAeZn0zVVNpTWW",
        "SOPHIE": "5a2w2tgpLwv26BYJf2qYwu"
    }

    # initialize Spotify Client Credentials object with app's client ID/secret
    spotify_credentials = SpotifyClientCredentials(
        client_id=os.environ['SPOTIPY_CLIENT_ID'],
        client_secret=os.environ['SPOTIPY_CLIENT_SECRET'])

    # Getting Spotify access token

    credential_token = spotify_credentials.get_access_token()

    # initialize Spotify as Spotipy object
    spotify = spotipy.Spotify(auth=credential_token)

    # Read coachella_artist10.json file and insert artist data
    with open('seed_data/coachella_artists10.json') as json_data:
        d = json.load(json_data)

        for row in d:
            name = row.get('artist')
            # print "Artist name from JSON: " + name
            url = row.get('website_url', None)
            img = row.get('image_url', None)

            results = spotify.search(q='artist:' + name, type='artist')

            # This errors out if the list is not in Spotify API and list is empty
            # artist_info = results['artists']['items'][0]

            # if list is empty, add to dictionary as None,
            # which will be changed to null when turned into a JSON object
            if not results['artists']['items']:
                spotify_id = None
                row['spotify_artist_id'] = spotify_id
                # print "New row with spot_id as None for", name, "\n", row, "\n\n"
                artist_info_list.append(row)

            #### (john) you can replace this with a dictionary:
            #### i.e. {"Bedouin": "5bKdC6382t97Qnpvs81Rqx",
            ####       "DESPACIO": None}
            #### etc

            # elif name == "Bedouin":
            #     spotify_id = "5bKdC6382t97Qnpvs81Rqx"
            # ...

            elif name in not_first_result:
                spotify_id = not_first_result[name]

            # else... not an empty list, add spotify_artist_id to the db
            # add key:value pair into dictionary, to be added to be dictionary,
            # which will be turned into a JSON object, so I do not need to keep
            # calling the Spotify API when seeding my db.
            else:
                artist_info = results['artists']['items'][0]
                # print "Artist name from Spotify:", artist_info['name'], "\n"
                # print artist_info
                # adding Spotify Artist ID to variable
                spotify_id = artist_info['id']
                # print spotify_id

                # add a new key:value pair to add to row
                row['spotify_artist_id'] = spotify_id
                # print "New row with spot_id for", name, "\n", row, "\n\n"
                artist_info_list.append(row)

                # Check if artist name from Coachella list is the same
                # as artist name from Spotify, if not add to
                # not_the_same dictionary {coachella name: spotify name}
                # if name.lower() != artist_info['name'].lower():
                #     name_not_same[name] = artist_info['name']

            #### TO DO!!!! make request from spotify --> probably function call ####

            artist = Artist(artist_name=name,
                            artist_url=url,
                            artist_img=img,
                            spotify_artist_id=spotify_id)

            # We need to add to the session or it won't ever be stored
            db.session.add(artist)

        # Once we're done, we should commit our work
        db.session.commit()
        json_data.close

        # print "Artist names that do not match:\n", name_not_same

    # Convert artist_info_list into JSON object, export to .json file
    with open('seed_data/coachella_with_spotify.json', 'w') as coachella_spotify:
        json.dump(artist_info_list, coachella_spotify)
        coachella_spotify.close


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
            # print stage_info
            stage_id = stage_info.stage_id

            festival_artist = FestivalArtist(festival_id=1,
                                             artist_id=artist_id,
                                             day1_at=day1_playing,
                                             day2_at=day2_playing,
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
