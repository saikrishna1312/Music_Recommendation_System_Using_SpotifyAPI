# data_fetcher.py (modified for Render)

import pandas as pd
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3  
import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv()

# Spotify API credentials
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = Spotify(auth_manager=auth_manager)

# Database setup
db_connection = sqlite3.connect("music_recommendations.db", check_same_thread=False)
cursor = db_connection.cursor()

# Create a table to store song data if it doesn’t already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS songs (
    track_id TEXT PRIMARY KEY,
    name TEXT,
    artist TEXT,
    danceability REAL,
    energy REAL,
    tempo REAL,
    loudness REAL
)
""")
db_connection.commit()

def fetch_and_store_data():
    # List of playlists to fetch from for diversity
    playlist_ids = [
        "37i9dQZF1DXcBWIGoYBM5M",  # Today's Top Hits
        "37i9dQZF1DWXRqgorJj26U",  # Mood Booster
        "37i9dQZF1DX0XUsuxWHRQd",  # Chill Hits
        "37i9dQZF1DX1lVhptIYRda",  # RapCaviar
        "37i9dQZF1DX4JAvHpjipBk",  # New Music Friday
        "37i9dQZF1DX6VdMW310YC7",  # Hot Country
        "37i9dQZF1DX9tPFwDMOaN1",  # Rock Classics
        "37i9dQZF1DX4SBhb3fqCJd",  # All Out 80s
        "37i9dQZF1DX0MLFaUdXnjA",  # Peaceful Piano
        "37i9dQZF1DX2sUQwD7tbmL",  # Power Workout
        "37i9dQZF1DWY4xHQp97fN6",  # Beast Mode
        "37i9dQZF1DX4dyzvuaRJ0n",  # Jazz Classics
        "37i9dQZF1DWTJ7xPn4vNaz",  # Classical Essentials
        "37i9dQZF1DWV7EzJMK2FUI",  # Chill Vibes
        "37i9dQZF1DWYBF1dYDPlHw"   # Indie Pop
    ]

    for playlist_id in playlist_ids:
        playlist_tracks = sp.playlist_tracks(playlist_id)
        
        # Process each track and fetch audio features
        for item in playlist_tracks['items']:
            track = item['track']
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            features = sp.audio_features(track_id)[0]
            
            if features:
                # Insert or replace data in the database
                cursor.execute("""
                    INSERT OR REPLACE INTO songs (track_id, name, artist, danceability, energy, tempo, loudness)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (track_id, track_name, artist_name, features['danceability'], features['energy'], 
                      features['tempo'], features['loudness']))
    
    db_connection.commit()
    print("Data fetched and stored successfully.")

# Run the fetch function
fetch_and_store_data()
