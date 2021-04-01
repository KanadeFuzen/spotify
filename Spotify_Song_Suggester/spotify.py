from os import getenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from .models import DB, Track, Song_Cluster, Song_NN, Output
import joblib
from sklearn.neighbors import NearestNeighbors

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id="b18678fa3b0b462fa81b2524a14d9c6f",
        client_secret="81708b054032490c9f6762439d99e91a"))

def get_info_and_add(track_name):
    try:
        results = sp.search(q='"'+track_name+'"', type="track", limit=20)

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

def get_features_cluster(track_name):
    user_input = '"'+track_name+'"'
    search_results = sp.search(q=user_input, type="track", limit=1)
    search_id = search_results['tracks']['items'][0]['id']
    search_features = sp.audio_features(tracks=search_id)

    for_dict_cluster = Song_Cluster(acousticness=(search_features[0]['acousticness']),
                    danceability=(search_features[0]['danceability']),
                    duration_ms=(search_features[0]['duration_ms']), 
                    energy=(search_features[0]['energy']),
                    explicit=(search_results['tracks']['items'][0]['explicit']), 
                    instrumentalness=(search_features[0]['instrumentalness']),
                    key=(search_features[0]['key']), 
                    liveness=(search_features[0]['liveness']),
                    loudness=(search_features[0]['loudness']), 
                    mode=(search_features[0]['mode']),
                    popularity=(search_results['tracks']['items'][0]['popularity']), 
                    speechiness=(search_features[0]['speechiness']),
                    tempo=(search_features[0]['tempo']), 
                    valence=(search_features[0]['valence']))

    dictionary_cluster = {
                  'acousticness': [for_dict_cluster.acousticness],
                  'danceability': [for_dict_cluster.danceability], 
                  'duration_ms': [for_dict_cluster.duration_ms],
                  'energy': [for_dict_cluster.energy], 
                  'explicit': [for_dict_cluster.explicit],
                  'instrumentalness': [for_dict_cluster.instrumentalness], 
                  'key': [for_dict_cluster.key],
                  'liveness': [for_dict_cluster.liveness],
                  'loudness': [for_dict_cluster.loudness],
                  'mode': [for_dict_cluster.mode],
                  'popularity': [for_dict_cluster.popularity],
                  'speechiness': [for_dict_cluster.speechiness],
                  'tempo': [for_dict_cluster.tempo],
                  'valence': [for_dict_cluster.valence]}

    cluster_model_input_df = pd.DataFrame.from_dict(data=dictionary_cluster, orient='columns')

    return cluster_model_input_df

def get_features_nn(track_name):
    search_results = sp.search(q=track_name, type="track", limit=1)
    search_id = search_results['tracks']['items'][0]['id']
    search_features = sp.audio_features(tracks=search_id)

    for_dict_nn = Song_NN(acousticness=(search_features[0]['acousticness']),
                   danceability=(search_features[0]['danceability']),
                   disc_number=(search_results['tracks']['items'][0]['disc_number']), 
                   duration_ms=(search_features[0]['duration_ms']), 
                   energy=(search_features[0]['energy']), 
                   explicit=(search_results['tracks']['items'][0]['explicit']),
                   instrumentalness=(search_features[0]['instrumentalness']),
                   key=(search_features[0]['key']),
                   liveness=(search_features[0]['liveness']),
                   loudness=(search_features[0]['loudness']),
                   mode=(search_features[0]['mode']),
                   speechiness=(search_features[0]['speechiness']),
                   tempo=(search_features[0]['tempo']),
                   time_signature=(search_features[0]['time_signature']),
                   track_number=(search_results['tracks']['items'][0]['track_number']),
                   valence=(search_features[0]['valence']))

    dictionary_nn = {
              'acousticness': [for_dict_nn.acousticness],
              'danceability': [for_dict_nn.danceability],
              'disc_number': [for_dict_nn.disc_number],
              'duration_ms': [for_dict_nn.duration_ms],
              'energy': [for_dict_nn.energy],
              'explicit': [for_dict_nn.explicit],
              'instrumentalness': [for_dict_nn.instrumentalness],
              'key': [for_dict_nn.key],
              'liveness': [for_dict_nn.liveness],
              'loudness': [for_dict_nn.loudness],
              'mode': [for_dict_nn.mode],
              'speechiness': [for_dict_nn.speechiness],
              'tempo': [for_dict_nn.tempo],
              'time_signature': [for_dict_nn.time_signature],
              'track_number': [for_dict_nn.track_number],
              'valence': [for_dict_nn.valence]}

    nn_model_input_df = pd.DataFrame.from_dict(data=dictionary_nn, orient='columns')

    return nn_model_input_df

def get_predictions_nn(model_input):
    spotify = pd.read_csv('data/spotify.csv')
    spotify['artists'] = spotify['artists'].str.replace("'", "")
    spotify['artists'] = spotify['artists'].str.replace("[", "")
    spotify['artists'] = spotify['artists'].str.replace("]", "")
    nn_model = joblib.load('data/nearest_neighbors.sav')
    neigh_dist, neigh_ind = nn_model.kneighbors(model_input)

    most_similar = []

    for i in range(len(neigh_ind[0])):
        song = spotify.iloc[neigh_ind[0][i]]['name']
        artist = spotify.iloc[neigh_ind[0][i]]['artists']
        entry = Output(song, artist)
        most_similar.append(entry)

    most_similar = most_similar[1:]
    tracks = []

    for i in range(len(most_similar)):
        suggestion = most_similar[i].name+' by '+most_similar[i].artist
        tracks.append(suggestion)

    return tracks