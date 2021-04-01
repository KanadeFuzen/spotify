from os import getenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import DB, Track, Song_Cluster, Song_NN, Output
from .spotify import get_info_and_add, get_features_nn, get_predictions_nn

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)
    

    @app.route("/")
    def root():
        DB.drop_all()
        DB.create_all()
        tracks = Track.query.all()
        return render_template("base.html", tracks=tracks)
    
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="RESET", tracks=Track.query.all())


    @app.route("/user_submitted", methods=["GET", "POST"])
    def user_submitted():

        track_name = request.form
        #print(track_name, type(track_name))
        #print(track_name['track_name'])
        model_input = get_features_nn(track_name['track_name'])
        #DB_track = get_info_and_add(track_name['track_name'])
        #print('Contents of DB_track',DB_track)
        track_names = get_predictions_nn(model_input)
        print(track_names)

        return render_template("user.html", track_name=track_name['track_name'], tracks=track_names)
    
    return app
