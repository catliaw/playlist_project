from flask_sqlalchemy import SQLAlchemy
import datetime
import api_helper

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions


class Festival(db.Model):
    """Music festivals with artist lineup."""

    __tablename__ = "festivals"

    festival_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    festival_name = db.Column(db.String(50), nullable=False)
    festival_route = db.Column(db.String(30), nullable=False)
    festival_url = db.Column(db.String(100))
    # weekend1_start_at = db.Column(db.DateTime)
    # weekend1_range = db.Column(db.Integer)
    # weekend2_start_at = db.Column(db.DateTime)
    # weekend2_range = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Festival festival_id=%s festival_name=%s>" % (self.festival_id,
                                                               self.festival_name)


class Stage(db.Model):
    """Stages at a specific music festival."""

    __tablename__ = "stages"

    stage_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stage_name = db.Column(db.String(30), nullable=False)
    festival_id = db.Column(db.Integer, db.ForeignKey('festivals.festival_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Stage stage_id=%s stage_name=%s>" % (self.stage_id,
                                                      self.stage_name)


class FestivalArtist(db.Model):
    """Relational table for festivals and artists."""

    __tablename__ = "festival_artists"

    festival_artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    festival_id = db.Column(db.Integer, db.ForeignKey('festivals.festival_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))
    # weekend1_at = db.Column(db.DateTime)
    # weekend2_at = db.Column(db.DateTime)
    day1_at = db.Column(db.DateTime)
    day2_at = db.Column(db.DateTime)
    stage_id = db.Column(db.Integer, db.ForeignKey('stages.stage_id'))

    # Define relationship to festival
    festival = db.relationship("Festival",
                               backref=db.backref("festivalartists",
                               order_by=festival_artist_id))

    # Define relationship to artist
    artist = db.relationship("Artist",
                             backref=db.backref("festivalartists",
                             order_by=festival_artist_id))

    #Define relationship to stage
    stage = db.relationship("Stage",
                            backref=db.backref("festivalartists",
                            order_by=festival_artist_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<FestivalArtist festival_artist_id=%s festival_id=%s artist_id=%s>" % (self.festival_artist_id,
                                                                                       self.festival_id,
                                                                                       self.artist_id)


class Artist(db.Model):
    """Artist of festival lineup."""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(75), nullable=False)
    artist_url = db.Column(db.String(100))
    artist_img = db.Column(db.String(300))
    artist_bio = db.Column(db.String(300))
    spotify_artist_id = db.Column(db.String(50))
    top10_updated_at = db.Column(db.DateTime)


    def __repr__(self):
        """Provide helpful representation when printed."""

        encoded_name = self.artist_name.encode("utf-8")

        return "<Artist artist_id=%s artist_name=%s>" % (self.artist_id,
                                                         encoded_name)


class Song(db.Model):
    """Songs of an artist."""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(150), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)
    spotify_track_id = db.Column(db.String(50))

    playlists = db.relationship('Playlist',
                               secondary='playlist_songs',
                               backref='songs')

    def __repr__(self):
        """Provide helpful representation when printed."""

        encoded_name = self.song_name.encode("utf-8")

        return "<Song song_id=%s song_name=%s>" % (self.song_id,
                                                   encoded_name)


class PlaylistSong(db.Model):
    """Association table connecting playlists and songs."""

    # This is an association table; it does not contain any interesting fields
    # Noelis would call it 'Frankentable'

    __tablename__ = "playlist_songs"

    playlist_song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<PlaylistSong playlist_song_id=%s playlist_id=%s song_id=%s>" % (self.playlist_song_id,
                                                                                 self.playlist_id,
                                                                                 self.song_id)


class Playlist(db.Model):
    """Playlist of songs for Spotify and displaying."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    playlist_name = db.Column(db.String(100))
    spotify_playlist_id = db.Column(db.String(50))
    spotify_playlist_url = db.Column(db.String(300))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Playlist playlist_id=%s user_id=%s>" % (self.playlist_id,
                                                         self.user_id)


class User(db.Model):
    """User who registers for an account."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_spot_id = db.Column(db.String(50), nullable=False)
    # Large field for password when need to create hash for secure login
    # user_password = db.Column(db.String(500), nullable=False)
    # user_fname = db.Column(db.String(45))
    # user_lname = db.Column(db.String(45))

    def __repr__(self):
        """Provide helpful representation when printed."""

        encoded_spot_id = self.user_spot_id.encode("utf-8")

        return "<User user_id=%s user_email=%s>" % (self.user_id,
                                                    encoded_spot_id)


##############################################################################
# Helper functions

def add_new_user(spotify_userid):
    """Check if user in DB; if not, add new user to DB."""

    user_in_db = User.query.filter_by(user_spot_id=spotify_userid).first()
    print "\nChecking for", spotify_userid, "in the db!\n"

    if user_in_db is None:
        print "\n", spotify_userid, "is not in the db!\n"
        new_user = User(user_spot_id=spotify_userid)
        db.session.add(new_user)
        db.session.commit()
        print "\n", spotify_userid, "was added to the db!\n"
    else:
        print "\n", spotify_userid, "was already in the db!\n"


def add_top10_tracks(new_top10_tracks, artist_db_id):
    for track in new_top10_tracks:
        track_name = track['name']
        track_id = track['id']

        new_song = Song(song_name=track_name,
                        artist_id=artist_db_id,
                        spotify_track_id=track_id)

        db.session.add(new_song)


def add_top10_tracks_check(new_top10_tracks, artist_db_id):
    for track in new_top10_tracks:
        track_name = track['name']
        track_id = track['id']

        if not Song.query.filter_by(spotify_track_id=track_id).first():

            new_song = Song(song_name=track_name,
                            artist_id=artist_db_id,
                            spotify_track_id=track_id)

            db.session.add(new_song)


def parse_commit_top10(recently_updated,
                       today,
                       spotify,
                       spotify_artist_uri,
                       artist_db_info,
                       artist_db_id):

    if recently_updated is None:

        new_top10_tracks = api_helper.spotify_top10(spotify_artist_uri, spotify)

        add_top10_tracks(new_top10_tracks, artist_db_id)

    elif recently_updated < (today - datetime.timedelta(days=7)):

        new_top10_tracks = api_helper.spotify_top10(spotify_artist_uri, spotify)
        # to test whether track updating works after however many days/time set
        # new_top10_tracks.append({'name': 'haaaaay', 'id': 'NOT AN ID HAHAHAHAHA'})
        print "\n\n top10_updated_at has been updated!!!!!!"

        add_top10_tracks_check(new_top10_tracks, artist_db_id)

    artist_db_info.top10_updated_at = today
    db.session.commit()


def check_db_top10(artist_db_id, artist_db_info):
    top_songs = Song.query.filter_by(artist_id=artist_db_id).all()
    print "\n\n", artist_db_info.artist_name, top_songs

    return top_songs


def connect_to_db(app, db_uri='postgresql:///playfest'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."