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

class Song_Cluster:
  def __init__(self, acousticness, danceability, duration_ms, energy, 
               explicit, instrumentalness, key, liveness, loudness, mode,
               popularity, speechiness, tempo, valence):
                  self.acousticness = acousticness
                  self.danceability = danceability
                  self.duration_ms = duration_ms
                  self.energy = energy
                  self.explicit = explicit
                  self.instrumentalness = instrumentalness
                  self.key = key
                  self.liveness = liveness
                  self.loudness = loudness
                  self.mode = mode
                  self.popularity = popularity
                  self.speechiness = speechiness
                  self.tempo = tempo
                  self.valence = valence

class Song_NN:
  def __init__(self, acousticness, danceability, disc_number, duration_ms, energy, 
               explicit, instrumentalness, key, liveness, loudness, mode, 
               speechiness, tempo, time_signature, track_number, valence):
                  self.acousticness = acousticness
                  self.danceability = danceability
                  self.disc_number = disc_number
                  self.duration_ms = duration_ms
                  self.energy = energy
                  self.explicit = explicit
                  self.instrumentalness = instrumentalness
                  self.key = key
                  self.liveness = liveness
                  self.loudness = loudness
                  self.mode = mode
                  self.speechiness = speechiness
                  self.tempo = tempo
                  self.time_signature = time_signature
                  self.track_number = track_number
                  self.valence = valence

class Output:
  def __init__(self, name, artist):
    self.name = name
    self.artist = artist