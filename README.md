# Hybrid Music Recommendation System 🎶

This project is a **Hybrid Music Recommendation System** that uses **Spotify API** to fetch song data and audio features from various popular playlists. 
**Content-Based Filtering**: Recommends songs with similar audio features (e.g., danceability, energy, tempo) by calculating cosine similarity between tracks in the database.

**Collaborative Filtering**: Due to the absence of explicit user ratings or historical listening data, collaborative filtering is implemented using a similarity matrix based on shared playlists, simulating song co-occurrences. While this method approximates collaborative filtering, it has limitations:
   - **No User-Specific History**: Recommendations are based on general song similarities rather than individualized preferences, making them less personalized than traditional collaborative filtering.
   - **Playlist-Based Data**: The system relies on song co-occurrences in playlists rather than actual user interactions, so recommendations may be limited by playlist diversity.

Despite these limitations, the hybrid approach effectively combines content and collaborative similarities to deliver diverse and relevant song recommendations.


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
