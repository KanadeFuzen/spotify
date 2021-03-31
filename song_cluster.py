import pandas as pd
import numpy as np
import sklearn
import tensorflow as tf
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score


class SongClusters():
  columns = ['acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
       'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity',
       'speechiness', 'tempo', 'valence']
  def __init__(self, dataframe):
    # Initialize dataframes 
    self.df = dataframe
    self.df_lookup = None
    self.reduced_df = None
    self.labels = None
    self.node_distances = []
    self.minibatch = None
    self.clusters = None
    self.pca = None
  
  def clean_df(self):
    columns_to_drop = ['release_date', 'year','artists','name','id']
    self.df_lookup = df[columns_to_drop].copy()
    self.df.drop(columns=columns_to_drop, axis=1, inplace=True)
  
  def pca_compress(self, compress_val=3):
    self.pca = PCA(compress_val) # Reduce dimensionality to 3
    self.reduced_df = self.pca.fit_transform(self.df)
  
  def create_kmeans_model(self):
    optimal_clusters = 50 # Experimental deduction
    self.minibatch = MiniBatchKMeans(n_clusters=optimal_clusters)
    self.labels = self.minibatch.fit_predict(self.reduced_df)
    self.clusters = self.minibatch.cluster_centers_

  def create_eucledian_dist_table(self): # Clusters is an array of cluster centers, reduced_df is a PCA transformed df now an array
    #node_distances = []
    for nodes in self.reduced_df:
      
      label = self.minibatch.predict(nodes.reshape(1,-1))
      cluster_cen = self.clusters[label].reshape(1,-1)
      distance = self.calculate_eucledian_dist(nodes[0], cluster_cen)
      self.node_distances.append(distance)
    # Create a complete look up table for songs, cluster labels and local cluster distances
    self.df_lookup['labels'] = self.labels
    self.df_lookup['node_distances'] = self.node_distances
  
  def predict(self, song_data, number_of_songs=10):
    # song_data should only contain columns in columns variable above

    #columns_to_drop = ['release_date', 'year','artists','name','id']
    #song_data.drop(columns=columns_to_drop, axis=1, inplace=True)
    # if song_data.columns != self.columns:
    #   raise Exception("Sorry, your song should be in a dataframe with the appropriate features")
    song_data = self.pca.transform(song_data)
    print('transformation complete')
    song_label = self.minibatch.predict(song_data)
    print('Song Label in cluster generated: {}'.format(song_label[0]))
    song_distance = self.calculate_eucledian_dist(song_data, self.clusters[song_label])
    print('Calculated Song Distances: {}'.format(song_distance))
    # Create a batch lookup table with all songs in cluster that chosen song belongs
    song_lookup = self.df_lookup[self.df_lookup['labels'] == song_label[0]]
    print('Song look up complete {}'.format(len(song_lookup)))
    display(song_lookup.head())
    song_lookup = song_lookup[song_lookup['node_distances'] >= song_distance[0]]
    print('Sorted out songs with nodes greater than chosen song',song_lookup)

    similar_songs = []
    for i in range(number_of_songs):
      song_info = (song_lookup.iloc[i][3], song_lookup.iloc[i].artists, song_lookup.iloc[i].id)
      similar_songs.append(song_info)
    return similar_songs

  def calculate_eucledian_dist(self, p1, p2):
    squared_dist = np.sum((p1-p2)**2, axis=1)
    dist = np.sqrt(squared_dist)
    return dist