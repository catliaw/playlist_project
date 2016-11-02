import time
from flask_sqlalchemy import SQLAlchemy

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
    festival_url = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Festival festival_id=%s festival_name=%s>" % (self.festival_id,
                                                               self.festival_name)


class Stage(db.Model):
    """Stages at a specific music festival."""

    __tablename__ = "stages"

    stage_id = db.Columm(db.Integer, autoincrement=True, primary_key=True)
    stage_name = db.Column(db.String(30), nullable=False)
    festival_id = db.Column(db.Integer, db.ForeignKey('festivals.festival_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Stage stage_id=%s stage_name=%s festival_id=%s>" % (self.stage_id,
                                                                     self.stage_name,
                                                                     self.festival_id)


class FestivalArtist(db.Model):
    """Relational table for festivals and artists."""

    __tablename__ = "festival_artists"

    festival_artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    festival_id = db.Column(db.Integer, db.ForeignKey('festivals.festival_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))
    day1_playing = db.Column(db.DateTime)
    day2_playing = db.Column(db.DateTime)
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

        return "<FestivalArtist festival_artist_id=%s festival_id=%s artist_id=%>" % (self.festival_artist_id,
                                                                                      self.festival_id,
                                                                                      self.artist_id)


class Artist(db.Model):
    """Artist of festival lineup."""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(64), nullable=False)
    artist_URL = db.Column(db.String(100), nullable=True)
    artist_img = db.Column(db.String(300), nullable=True)
    artist_bio = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Artist artist_id=%s artist_name=%s>" % (self.artist_id,
                                                         self.artist_name)


class Song(db.Model):
    """Songs of an artist."""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)

    playlists = db.relationship('Playlist',
                               secondary='playlist_songs',
                               backref='songs')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Song song_id=%s song_name=%s>" % (self.song_id,
                                                   self.song_name)


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

    playlist_id = db.Columm(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    playlist_name = db.Column(db.String(100), nullable=True)
    spotify_playlist_url = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Playlist playlist_id=%s user_id=%s>" % (self.playlist_id,
                                                         self.user_id)


class User(db.Model):
    """User who registers for an account."""

    __tablename__ = "users"

    user_id = db.Columm(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(25), nullable=False)
    user_fname = db.Column(db.String(45), nullable=True)
    user_lname = db.Column(db.String(45), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s user_email=%s>" % (self.user_id,
                                                    self.user_email)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playfest'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."