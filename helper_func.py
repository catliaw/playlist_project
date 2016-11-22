#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import datetime

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

    dow_num = datetime.datetime.isoweekday(datetime_obj)
    dow = DAY_OF_WEEK[dow_num]
    return dow
