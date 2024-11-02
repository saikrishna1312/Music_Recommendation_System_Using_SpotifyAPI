# Hybrid Music Recommendation System 🎶

This project is a **Hybrid Music Recommendation System** that uses **Spotify API** to fetch song data and audio features from various popular playlists. It combines **content-based** and **collaborative filtering** techniques to provide personalized song recommendations based on track features like danceability, energy, tempo, and loudness. The data is stored in an **SQLite** database, and daily updates are scheduled with **APScheduler** to keep the database current.

## Features

- **Hybrid Recommendation System**: Combines content-based and collaborative filtering for more accurate and diverse recommendations.
- **Automated Data Fetching**: Pulls song data daily from multiple Spotify playlists, ensuring a dynamic and up-to-date recommendation pool.
- **Data Storage**: Uses SQLite for efficient storage and retrieval of song data, with support for automatic deduplication.
- **Scalable and Modifiable**: Designed to be extended with more playlists, additional audio features, and different recommendation weights.

## How It Works

1. **Data Fetching**: The app fetches tracks from a variety of Spotify playlists (e.g., "Today's Top Hits", "Mood Booster", "Chill Hits") using Spotify’s API.
2. **Feature Extraction**: For each song, it extracts audio features like danceability, energy, tempo, and loudness.
3. **Hybrid Recommendation**:
   - **Content-Based Filtering**: Recommends songs with similar audio features.
   - **Collaborative Filtering**: Uses a precomputed similarity matrix to recommend songs that frequently appear together in playlists.
4. **Automated Updates**: APScheduler is used to update the database daily, keeping recommendations fresh.


## Example Playlists
The app currently fetches data from these Spotify playlists:
   - Today's Top Hits
   - Mood Booster
   - Chill Hits
   - RapCaviar
   - New Music Friday
   - Hot Country
   - Rock Classics
   - Jazz Classics
   - Indie Pop
Feel free to add more playlists in data_fetcher.py for increased diversity.
