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
    """Manually load SnowGlobe festival information into database."""

    print "Festival Info"

    snowglobe = Festival(festival_name="SnowGlobe 2016",
                         festival_route="snowglobe-2016",
                         festival_url="http://snowglobemusicfestival.com/")

    db.session.add(snowglobe)

    db.session.commit()


def load_snowglobe_artists():
    """Load artist info from coachella_artist10.json into database."""

    print "SnowGlobe Artists"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate artists
    # Artist.query.delete()

    artist_info_list = []

    name_not_same = {}

    not_first_result = {
        "Big Baby Bruiser + Young Lat": None,
        "THATSOUND": None,
        "Cremes n Lotions": None,
        "MASCOLO": None,
        "Cassian": "1ChtRJ3f4rbv4vtz87i6CD",
        "Vincent": "3yjt1AlzEQZXvUPaSfSwCj",
        "Point Point": "5L67d6oZKOOmXcBcMMJdZZ"
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
    with open('seed_data/snowglobe_artists6.json') as json_data:
        d = json.load(json_data)

        for row in d:
            name = row.get('artist').strip()
            print "Artist name from JSON: " + name
            # url = row.get('website_url', None)
            # img = row.get('image_url', None)

            search_existing_artist = Artist.query.filter_by(artist_name=name).first()

            if search_existing_artist is None:

                results = spotify.search(q='artist:' + name, type='artist')

                # This errors out if the list is not in Spotify API and list is empty
                # artist_info = results['artists']['items'][0]

                # if list is empty, add to dictionary as None,
                # which will be changed to null when turned into a JSON object
                if not results['artists']['items']:
                    spotify_id = None
                    row['spotify_artist_id'] = spotify_id
                    print "New row with spot_id as None for", name, "\n", row, "\n\n"
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
                    print "Artist name from Spotify:", artist_info['name'], "\n"
                    print artist_info
                    # adding Spotify Artist ID to variable
                    spotify_id = artist_info['id']
                    print spotify_id

                    # add a new key:value pair to add to row
                    row['spotify_artist_id'] = spotify_id
                    print "New row with spot_id for", name, "\n", row, "\n\n"
                    artist_info_list.append(row)

                    # Check if artist name from Coachella list is the same
                    # as artist name from Spotify, if not add to
                    # not_the_same dictionary {coachella name: spotify name}
                    if name.lower() != artist_info['name'].lower():
                        name_not_same[name] = artist_info['name']

                    name = artist_info['name']

                #### TO DO!!!! make request from spotify --> probably function call ####

                artist = Artist(artist_name=name,
                                artist_url=None,
                                artist_img=None,
                                spotify_artist_id=spotify_id)

                # We need to add to the session or it won't ever be stored
                db.session.add(artist)

        # Once we're done, we should commit our work
        db.session.commit()
        json_data.close

        print "Artist names that do not match:\n", name_not_same

    # Convert artist_info_list into JSON object, export to .json file
    with open('seed_data/coachella_with_spotify.json', 'w') as coachella_spotify:
        json.dump(artist_info_list, coachella_spotify)
        coachella_spotify.close


def load_snowglobe_stages():
    """Load Snowglobe stage info."""

    print "Snowglobe Stages"

    # Read snowglobe_artists6.json file and insert stage data
    with open('seed_data/snowglobe_artists6.json') as json_data:
        d = json.load(json_data)

        festival_info = Festival.query.filter_by(festival_name="SnowGlobe 2016").first()
        fest_id = festival_info.festival_id

        stages = []

        for row in d:
            stage = row.get('stage', None).strip()

            if (stage not in stages) and (stage is not None):
                stages.append(stage)

                #Considering that Coachella is the only festival in db, index=1
                snowglobe_stage = Stage(stage_name=stage,
                                        festival_id=fest_id)

                db.session.add(snowglobe_stage)

            else:
                pass

        db.session.commit()


def load_festivalartists():
    """Load Coachella artist-festival-stage data into festival_artists relational table."""

    print "Coachella FestivalArtist"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate festival_artists rows
    # FestivalArtist.query.delete()

    # Read coachella_artist10.json file and insert festival artist data
    with open('seed_data/snowglobe_artists6.json') as json_data:
        d = json.load(json_data)

        for row in d:
            # print row
            artist_name = row.get('artist')
            # print artist_name
            day1 = row.get('playing_at').strip()

            artist_info = Artist.query.filter(Artist.artist_name.like(artist_name)).first()
            # print artist_info
            artist_id = artist_info.artist_id
            # print artist_id

            stage = row.get('stage', None)

            if day1:
                day1_formatted = day1[-5:] + "/2016"
                print "\n\nday1_formatted", day1_formatted, "\n\n"
                playing_at = datetime.strptime(day1_formatted, '%m/%d/%Y')
            else:
                playing_at = None

            stage_info = Stage.query.filter_by(stage_name=stage).first()
            # print stage_info
            stage_id = stage_info.stage_id

            festival_artist = FestivalArtist(festival_id=2,
                                             artist_id=artist_id,
                                             day1_at=playing_at,
                                             day2_at=None,
                                             stage_id=stage_id)

            db.session.add(festival_artist)

        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_festivals()
    load_snowglobe_artists()
    load_snowglobe_stages()
    load_festivalartists()
