# spotify
A collaboration on building a spotify recommender app

## APP FUNCTIONALITY DESCRIPTION
For our Unit Project, we were handed the task of developing a spotify playlist recommendation app.
The idea is to be able to receive input from the user (track name) and provide a recommendation of 5 songs
they would like to have on their playlist based on the their song choice.

## THE DATA
The dataset for this project was gotten from the Kaggle Spotify competition.
In addition to the artist name, song title and year of release, the data contained the following features which eventually became the defining features for our predictive model. 
**'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit', 
'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
'popularity', 'speechiness', 'tempo', 'valence'**
Our dataset had over 1.2million songs and their accompanying features.

## SOLUTION DESCRIPTION
In order to be able to utilize this dataset, we had to go with an unsupervised learning algorithm seeing as our data had no labels.
We went with the K-nearest-neighbor machine learning algorithm as our algorithm of choice for this problem.
Our app was built using Flask as its development framework for the front end and SQLAlchemy for handling the database end.
# Important Function Definitions:
Function Name: **get_info_and_add**
Description: Takes all of the relevant songs related to the user's choice track and puts them in an SQL Database. It utilizes the search function from the spotipy library.

Function Name: **get_features_cluster**
Description: Takes the user's choice track name and retrieves all of the relevant features associated with the track. Also prepares the input vector by inputing data into a single row pandas dataframe.

Function Name: **get_predictions_nn**
Description: Runs the input feature vector through our KNN model and uses the returned cluster information for the input vector in extracting 5 other songs that exist in the same cluster feature space. See diagramatic representation of clustered songs below.

![image](https://user-images.githubusercontent.com/74992587/113327635-30e0b480-92e9-11eb-8c7e-6b8bf3844a36.png)

## RUNNING OUR APP LOCALLY
Pull the repo into your local machine using git clone.
Run: export FLASK_APP=app.py
cd into your Spotify_Song_Suggester directory
Run: flask run


## CREDITS
This project was made possible by the following contributors:

Joe Costa (https://github.com/jcost875) 

Murat Benbanaste (https://github.com/mbenbanaste) 

Kanade Fuzen (https://github.com/KanadeFuzen) 

Laurence Obi (https://github.com/afroroboticist) 
