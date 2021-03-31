from os import getenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import DB, Track
from .spotify import get_info_and_add

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
    
    
    @app.route("/user_submitted", methods=["GET", "POST"])
    def user_submitted():

        track_name = request.form
        print(track_name, type(track_name))
        print(track_name['track_name'])
        DB_track = get_info_and_add(track_name['track_name'])
        print('Contents of DB_track',DB_track)
        track_names = Track.query.all()

        return render_template("user.html", track_name=track_name['track_name'], tracks=track_names)
    
    return app




# import uvicorn
# from fastapi import FastAPI

# app = FastAPI()

# @app.get('/')
# def home():
#     return {'hello': 'world'}

# if __name__ == '__main__':
#     uvicorn.run(app)