import os
import time
import base64
import json
from dotenv import load_dotenv
from requests import get, post, HTTPError
from bs4 import BeautifulSoup

# Load environment variables from a .env file
load_dotenv()

# Spotify Credentials
SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Genius Credentials
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")

def get_spotify_token():
    """Obtains an access token from the Spotify API."""
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64}
    data = {"grant_type": "client_credentials"}
    
    try:
        result = post(url, headers=headers, data=data)
        result.raise_for_status()
        return result.json().get("access_token")
    except HTTPError as http_err:
        print(f"Spotify HTTP error (token): {http_err}")
    return None

def get_spotify_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    """Searches for an artist on Spotify to get their ID."""
    url = "https://api.spotify.com/v1/search"
    headers = get_spotify_auth_header(token)
    params = {"q": artist_name, "type": "artist", "limit": 1}

    try:
        result = get(url, headers=headers, params=params)
        result.raise_for_status()
        artists = result.json().get("artists", {}).get("items", [])
        return artists[0] if artists else None
    except HTTPError as http_err:
        print(f"Spotify HTTP error (artist search): {http_err}")
    return None

def get_artist_albums(token, artist_id):
    """Gets all official albums for a given artist from Spotify."""
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_spotify_auth_header(token)
    params = {"include_groups": "album", "limit": 50}
    
    try:
        result = get(url, headers=headers, params=params)
        result.raise_for_status()
        return result.json().get("items", [])
    except HTTPError as http_err:
        print(f"Spotify HTTP error (albums): {http_err}")
    return []

def get_album_tracks(token, album_id):
    """Gets all tracks for a given album from Spotify."""
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_spotify_auth_header(token)
    params = {"limit": 50}
    
    try:
        result = get(url, headers=headers, params=params)
        result.raise_for_status()
        return result.json().get("items", [])
    except HTTPError as http_err:
        print(f"Spotify HTTP error (tracks): {http_err}")
    return []

def search_genius_for_song_url(artist_name, track_title):
    """Searches Genius for a song and returns the URL of the top hit."""
    genius_search_url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    search_query = f"{track_title} {artist_name}"
    params = {'q': search_query}

    try:
        result = get(genius_search_url, headers=headers, params=params, timeout=5)
        result.raise_for_status()
        hits = result.json().get("response", {}).get("hits", [])
        for hit in hits:
            hit_artist = hit["result"]["primary_artist"]["name"]
            if artist_name.lower() in hit_artist.lower():
                return hit["result"]["url"]
        return None
    except HTTPError as http_err:
        print(f"Genius HTTP error: {http_err}")
    except Exception as err:
        print(f"An error occurred searching Genius: {err}")
    return None

def scrape_lyrics_from_genius(url):
    """Scrapes lyrics from a Genius.com URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        page = get(url, headers=headers, timeout=5)
        page.raise_for_status()
        
        soup = BeautifulSoup(page.text, "html.parser")
        lyrics_div = soup.find("div", attrs={"data-lyrics-container": "true"})
        if not lyrics_div:
            return "Could not find lyrics container on page."
            
        lyrics = lyrics_div.get_text(separator="\n")
        return lyrics.strip()
        
    except HTTPError as http_err:
        return f"HTTP error occurred while scraping: {http_err}"
    except Exception as err:
        return f"An error occurred while scraping: {err}"


# --- Main execution ---
if __name__ == "__main__":
    all_tracks_data = []
    ARTIST_NAME_TO_SEARCH = "Mac Miller"
    
    spotify_token = get_spotify_token()
    if spotify_token:
        artist = search_for_artist(spotify_token, ARTIST_NAME_TO_SEARCH)
        
        if artist:
            print(f"Found artist: {artist['name']} (Spotify ID: {artist['id']})")
            albums = get_artist_albums(spotify_token, artist['id'])
            
            target_album_name = "Balloonerism"
            target_album = next((a for a in albums if a['name'] == target_album_name), None)

            if target_album:
                print(f"--- Processing Album: {target_album['name']} ---")
                tracks = get_album_tracks(spotify_token, target_album['id'])
                
                if tracks:
                    for track in tracks:
                        track_name = track['name']
                        print(f"Fetching data for track: {track_name}...")
                        
                        time.sleep(0.3)
                        genius_url = search_genius_for_song_url(artist['name'], track_name)
                        
                        lyrics = "Not found"
                        if genius_url:
                           lyrics = scrape_lyrics_from_genius(genius_url)

                        all_tracks_data.append({
                            'artist': artist['name'],
                            'album': target_album['name'],
                            'track_title': track_name,
                            'genius_url': genius_url if genius_url else "Not Found",
                            'lyrics': lyrics
                        })
    
  
if all_tracks_data:
    
    output_dir = 'data'
    file_name = 'Swimming2.jsonl' # Or 'Balloonerism.jsonl', etc.
    
    
    os.makedirs(output_dir, exist_ok=True)
    
  
    jsonl_file = os.path.join(output_dir, file_name)
    
    print(f"\nWriting {len(all_tracks_data)} tracks to {jsonl_file}...")
    
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for record in all_tracks_data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
            
    print("Done!")
