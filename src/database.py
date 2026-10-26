"""
vamos a crear una bd para evitar duplicidad
is a Relational Model with 2 tables: tracks and listens

"""
import sqlite3
import pandas as pd
from pathlib import Path

def init_db(db_path: str):
    """Creates the data base scheme if it does not previously exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # dimension table (Tracks)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_uri TEXT PRIMARY KEY,
            track_name TEXT,
            artist_name TEXT,
            album_name TEXT
        )
    ''')
    
    # transaction table (Listens) 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_uri TEXT,
            played_at TIMESTAMP,
            ms_played INTEGER,
            reason_start TEXT,
            reason_end TEXT,
            shuffle BOOLEAN,
            skipped BOOLEAN,
            FOREIGN KEY (track_uri) REFERENCES tracks (track_uri)
        )
    ''')
    
    conn.commit()
    return conn

def load_data_to_db(parquet_path: str, conn: sqlite3.Connection):
    """Loads the data from Parquet to the relational model."""
    print("Reading Parquet file...")
    df = pd.read_parquet(parquet_path)
    
    # 1. handle Null URIs (some local tracks do not have Spotify URI).
    # we filter them to keep referential integrity.
    df = df.dropna(subset=['track_uri'])
    
    # 2. Extract data from Tracks (without duplicates)
    tracks_df = df[['track_uri', 'track_name', 'artist_name', 'album_name']].drop_duplicates(subset=['track_uri'])
    
    # 3. Extract data from Listens
    listens_df = df[['track_uri', 'played_at', 'ms_played', 'reason_start', 'reason_end', 'shuffle', 'skipped']]
    
    print(f"Inserting {len(tracks_df)} unique songs in 'Tracks' table...")
    tracks_df.to_sql('tracks', conn, if_exists='replace', index=False)
    
    print(f"Inserting {len(listens_df)} reproductions in 'Listens' table...")
    listens_df.to_sql('listens', conn, if_exists='replace', index=False)
    
    print("Load completed succesfully!")

if __name__ == "__main__":
    PARQUET_FILE = "data/processed/spotify_clean.parquet"
    DB_FILE = "spotify_data.db"
    
    if not Path(PARQUET_FILE).exists():
        print("Error: No Parquet file found. Run etl.py first.")
    else:
        # initialize BD and load data
        conexion = init_db(DB_FILE)
        load_data_to_db(PARQUET_FILE, conexion)
        conexion.close()
