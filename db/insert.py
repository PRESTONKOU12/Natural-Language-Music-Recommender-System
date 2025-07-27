def insert_artist(cursor, artist):
    cursor.execute('''
        INSERT INTO artists (artist_id, name) 
            VALUES (%s, %s) 
            ON CONFLICT (artist_id) DO NOTHING;''', 
    (artist['id'], artist['name']))

def insert_track(cursor, track, artist_id, playlist_id):
    cursor.execute('''
        INSERT INTO tracks (track_id, track_name, artist_id, playlist_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (track_id) DO NOTHING;''',
    (track['id'], track['name'], artist_id, playlist_id))

def insert_playlist(cursor, playlist):
    cursor.execute('''
        INSERT INTO playlists (playlist_id, name, description, total_tracks, source_tag)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (playlist_id) DO NOTHING''',
    (playlist['id'], playlist['name'], playlist['description'], playlist['total_tracks'], playlist['source_tag']))

def insert_audio_features(cursor, af):
    cursor.execute("""
        INSERT INTO audio_features (
            track_id, danceability, energy, key, loudness, mode,
            speechiness, acousticness, instrumentalness, liveness,
            valence, tempo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (track_id) DO NOTHING;
    """, (
        af['id'], af['danceability'], af['energy'], af['key'],
        af['loudness'], af['mode'], af['speechiness'],
        af['acousticness'], af['instrumentalness'],
        af['liveness'], af['valence'], af['tempo']
    ))