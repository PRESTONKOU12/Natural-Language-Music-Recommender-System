import psycopg2 #type: ignore
import spotipy #type: ignore
import json 
import time
from config import DB_PARAMS, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from db import create_tables, insert_artist, insert_track, insert_playlist, insert_audio_features

#Loads the playlist json file. 
def load_playlists_from_file(filepath = "playlists.json"):
    with open(filepath, 'r') as file:
        return json.load(file)


def load_playlist_tracks(sp, playlist_url, cursor):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id, additional_types = ['track'])

    while results:
        for item in results['items']:
            track = item.get('track')
            if not track or not track['id']:
                continue  # skip local/unavailable
            
            insert_playlist(cursor, playlist_id)

            # Insert artist
            artist = track['artists'][0]
            insert_artist(cursor, artist)

            # Insert track
            insert_track(cursor, track, artist['id'], playlist_id)

            # Get and insert audio features
            af = sp.audio_features(track['id'])[0]
            if af:
                insert_audio_features(cursor, af)

        if results['next']:
            results = sp.next(results)
        else:
            results = None

def is_playlist_loaded(cursor, playlist_id):
    cursor.execute("SELECT 1 FROM loaded_playlists WHERE playlist_id = %s;", (playlist_id,))
    return cursor.fetchone() is not None

def mark_playlist_loaded(cursor, playlist_id):
    cursor.execute("INSERT INTO loaded_playlists (playlist_id) VALUES (%s) ON CONFLICT DO NOTHING;", (playlist_id,))


if __name__ == "__main__":
    playlists = load_playlists_from_file()
    try:
        sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET
                ))
    except Exception as e:
        print(f'Unable to connect to spotify: {e}')

    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cursor:
                create_tables(cursor)
                conn.commit()
                for pl in playlists:
                    print(f'Loading: {pl['name']}')
                    try:
                        load_playlist_tracks(sp, pl['url'], cursor)
                    except Exception as e:
                        print(f'Failed loading playlist {pl['name']}: {e}')
                        conn.rollback()
                    time.sleep(1)
                
                print('Done Populating Database!')

    except Exception as e:
        print(f'Unable to connect to database:| {e}')

    
