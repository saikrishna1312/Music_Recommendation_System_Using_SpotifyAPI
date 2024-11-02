from flask import Flask, request, render_template
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import dotenv
import os

# Spotify API credentials
dotenv.load_dotenv()

# Retrieve client ID and secret from the .env file
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = Spotify(auth_manager=auth_manager)

app = Flask(__name__)
db_connection = sqlite3.connect("music_recommendations.db", check_same_thread=False)

# Load song data and create the collaborative similarity matrix
def load_data_and_create_similarity_matrix():
    query = "SELECT * FROM songs"
    df = pd.read_sql(query, db_connection)
    
    # Data cleaning: Drop rows with missing feature values and ensure all features are numeric
    df = df.dropna(subset=['danceability', 'energy', 'tempo', 'loudness'])
    df[['danceability', 'energy', 'tempo', 'loudness']] = df[['danceability', 'energy', 'tempo', 'loudness']].apply(pd.to_numeric, errors='coerce')
    
    # Calculate collaborative similarity matrix using song features
    features = df[['danceability', 'energy', 'tempo', 'loudness']]
    similarity_matrix = cosine_similarity(features)
    
    # Create a DataFrame with song IDs as both rows and columns
    collaborative_sim_matrix = pd.DataFrame(
        similarity_matrix,
        index=df['track_id'],
        columns=df['track_id']
    )
    return df, collaborative_sim_matrix

# Load data and similarity matrix at startup
df, collaborative_sim_matrix = load_data_and_create_similarity_matrix()

def get_song_features_from_spotify(song_name):
    # Use Spotify's search API to find the track
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_id = track['id']
        features = sp.audio_features(track_id)[0]
        return {
            'track_id': track_id,
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'danceability': features['danceability'],
            'energy': features['energy'],
            'tempo': features['tempo'],
            'loudness': features['loudness']
        }
    return None

def get_hybrid_recommendations(song_name):
    # Query the database for song features
    query = "SELECT * FROM songs"
    df = pd.read_sql(query, db_connection)

    # Data cleaning
    df = df.dropna(subset=['danceability', 'energy', 'tempo', 'loudness'])
    df[['danceability', 'energy', 'tempo', 'loudness']] = df[['danceability', 'energy', 'tempo', 'loudness']].apply(pd.to_numeric, errors='coerce')

    # Try finding the song by name in the database
    track = df[df['name'].str.lower() == song_name.lower()]
    
    if track.empty:
        print("Song not found in database. Fetching from Spotify API.")
        # If the song is not found in the database, fetch it from Spotify
        spotify_song = get_song_features_from_spotify(song_name)
        if spotify_song is None:
            print("Song not found on Spotify.")
            return []

        # Add the song features to the DataFrame temporarily for recommendation calculation
        track = pd.DataFrame([spotify_song])

    # Content-based recommendations: Calculate content similarity
    feature_vectors = df[['danceability', 'energy', 'tempo', 'loudness']].values
    content_similarities = cosine_similarity(
        track[['danceability', 'energy', 'tempo', 'loudness']],
        feature_vectors
    ).flatten()
    df['content_similarity'] = content_similarities

    # Collaborative recommendations: Use the collaborative similarity matrix
    song_id = track['track_id'].values[0]
    if song_id in collaborative_sim_matrix:
        df['collaborative_similarity'] = collaborative_sim_matrix[song_id]
    else:
        df['collaborative_similarity'] = 0  # or handle differently if no collaborative data is available

    # Fill NaN values in collaborative similarity with 0
    df['collaborative_similarity'] = df['collaborative_similarity'].fillna(0)

    # Calculate hybrid score with weights
    content_weight = 0.7
    collaborative_weight = 0.3
    df['hybrid_score'] = (content_weight * df['content_similarity'] +
                          collaborative_weight * df['collaborative_similarity'])

    # Exclude the input song from recommendations
    recommendations = df[df['track_id'] != song_id].sort_values(by='hybrid_score', ascending=False).head(5)
    print("Recommendations generated:", recommendations[['name', 'artist', 'hybrid_score']])

    return recommendations[['name', 'artist', 'hybrid_score']].to_dict(orient='records')

# Define Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    song_name = request.form.get('song_name')
    recommendations = get_hybrid_recommendations(song_name)
    return render_template('index.html', recommendations=recommendations, song_name=song_name)

if __name__ == '__main__':
    app.run(debug=True)
