import psycopg2 #type: ignore

def create_tables(cursor):
    #cursor.execute('DROP TABLE IF EXISTS audio_features;')
    #cursor.execute('DROP TABLE IF EXISTS tracks;')
    #cursor.execute('DROP TABLE IF EXISTS artists;')
    #cursor.execute('DROP TABLE IF EXISTS playlists;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            artist_id TEXT PRIMARY KEY,
            name varchar(40)
        ); ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            playlist_id TEXT PRIMARY KEY,
            name varchar(40) NOT NULL,
            description TEXT,
            total_tracks INTEGER,
            source_tag varchar(40)
        );  ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_id varchar(40) PRIMARY KEY,
            track_name varchar(40) NOT NULL,
            artist_id varchar(40),
            playlist_id varchar(40),
            FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
        ); ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_features (
            track_id TEXT PRIMARY KEY,
            danceability FLOAT,
            energy FLOAT,
            key INTEGER,
            loudness FLOAT,
            mode INTEGER,
            speechiness FLOAT,
            acousticness FLOAT,
            instrumentalness FLOAT,
            liveness FLOAT,
            valence FLOAT,
            tempo FLOAT,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id)
        ); ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loaded_playlists (
                playlist_id TEXT PRIMARY KEY,
                last_loaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );''')
