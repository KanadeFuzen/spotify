from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Track(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    track_id = DB.Column(DB.String(50), nullable=False)
    track = DB.Column(DB.String(50), nullable=False)
    artist = DB.Column(DB.String(50), nullable=False)
    album = DB.Column(DB.String(50), nullable=False)

    def __repr__(self):
        return "<Track {}>".format(self.track)