from os import getenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import DB, Track

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id="b18678fa3b0b462fa81b2524a14d9c6f",
        client_secret="81708b054032490c9f6762439d99e91a"))

def get_info_and_add(track_name):
    try:
        track_name='Dance with father'
        results = sp.search(q='Dance with father', type="track", limit=20)

        for count, DB_track in enumerate(results['tracks']['items']):
            track_id = results['tracks']['items'][count]['id']
            track = results['tracks']['items'][count]['name']
            artist = results['tracks']['items'][count]['artists'][0]['name']
            album = results['tracks']['items'][count]['album']['name']
            
            DB_track = Track(
                track_id=track_id,
                track=track,
                artist=artist,
                album=album
                )
            DB.session.add(DB_track)
            DB.session.commit()
    
        return DB_track

    except Exception as e:
        print("Error Processing %s: %s" % (track_name, e))



# track_id_list = []
#         tracks_list = []
#         artists_list = []
#         albums_list = []

#         for count, track_id in enumerate(results['tracks']['items']):
#             track_id = results['tracks']['items'][count]['id']
#             track_id_list.append(track_id)

#         for count, track in enumerate(results['tracks']['items']):
#             track = results['tracks']['items'][count]['name']
#             tracks_list.append(track)
        
#         for count, artist in enumerate(results['tracks']['items']):
#             artist = results['tracks']['items'][count]['artists'][0]['name']
#             artists_list.append(artist)
           
#         for count, album in enumerate(results['tracks']['items']):
#             album = results['tracks']['items'][count]['album']['name']
#             albums_list.append(album)
        
#         DB_track = Track(
#             track_id=track_id_list,
#             track_name=tracks_list,
#             artist=artists_list,
#             album=albums_list
#             )
        
#         DB.session.add(DB_track)
#         DB.session.commit()