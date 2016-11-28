#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import datetime
import model
import helper_func
import api_helper

# make datetime_to_dow function in separate file
DAY_OF_WEEK = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'}


def create_playlist_name(user_playlist_name):
    """Format playlist name."""

    playfest_prefix = u"\u266A Playfest \u266B "
    playlist_name = playfest_prefix + user_playlist_name

    return playlist_name


def datetime_to_dow(datetime_obj):
    """Change datetime object to day of the week string."""

    dow_num = datetime.datetime.isoweekday(datetime_obj)
    dow = DAY_OF_WEEK[dow_num]
    return dow


def shuffle_pick_songs(top_songs):
    """Shuffle top 10 songs and randomly select 3 songs."""
    random.shuffle(top_songs)
    random_songs = top_songs[0:3]

    return random_songs


def build_playlist_json(random_songs, artist_db_info, song_name_id, playlist_json):
    """Format playlist JSON {"artist1": {"title 1": id1, "title2": id2}, "artist2"}"""

    # for each song, create key-value as such: "title 1": id1 in dict song_name_id
    for song in random_songs:
        song_name_id[song.song_name] = song.spotify_track_id

    # for each artist, pack artist name and song information as such:
    # {"artist1": {"title 1": id1, "title2": id2}, "artist2"...}
    playlist_json[artist_db_info.artist_name] = song_name_id
    print "\n\nplaylist_json after adding", artist_db_info.artist_name, playlist_json


def parse_artist_to_playlist(playlist_json, playlist_artists, spotify):
    """Loop through artists to find top 10 songs, add to db, add to playlist_json."""
    for artist in playlist_artists:
        artist_db_info = model.Artist.query.filter_by(artist_name=artist).first()
        artist_db_id = artist_db_info.artist_id
        spotify_artist_uri = 'spotify:artist:' + artist_db_info.spotify_artist_id
        recently_updated = artist_db_info.top10_updated_at
        # print "\n\n", artist_db_info.artist_name, "recently_updated", recently_updated
        today = datetime.datetime.today()
        # print "today", today

        model.parse_commit_top10(recently_updated,
                                 today,
                                 spotify,
                                 spotify_artist_uri,
                                 artist_db_info,
                                 artist_db_id)

        top_songs = model.check_db_top10(artist_db_id, artist_db_info)

        random_songs = helper_func.shuffle_pick_songs(top_songs)

        song_name_id = {}

        helper_func.build_playlist_json(random_songs,
                                        artist_db_info,
                                        song_name_id,
                                        playlist_json)


def build_lineup_list(artist_list, artist_info):
    """Loop festival's artists to gather info for Jinja and festival specific page."""
    for artist in artist_list:
        name = artist.artist.artist_name
        # print "\n\nName of artist:", name
        spotify_id = artist.artist.spotify_artist_id
        # print "\nSpotify ID:", spotify_id
        day1_datetime = artist.day1_at
        # print "\nDatetime:", day1_datetime
        dow_num = datetime.datetime.isoweekday(day1_datetime)
        # day1_dow = helper_func.datetime_to_dow(day1_datetime)
        # print "\nDay of the :", day1_dow
        stage = artist.stage.stage_name
        # print "\nStage:", stage, "\n"

        artist_info.append({
            "artist_name": name,
            "spotify_artist_id": spotify_id,
            "playing_on": dow_num,
            "stage": stage
            })
        # print "\nArtist Info List:", artist_info, "\n"
