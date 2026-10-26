import sqlite3
import pandas as pd

def run_analytical_queries(db_path: str):
    """Runs analytical SQL queries against the database."""
    conn = sqlite3.connect(db_path)
    
    print("--- Top 5 Most Played Artists ---")
    query_artists = """
        SELECT t.artist_name, COUNT(l.track_uri) as play_count
        FROM listens l
        JOIN tracks t ON l.track_uri = t.track_uri
        GROUP BY t.artist_name
        ORDER BY play_count DESC
        LIMIT 5;
    """
    print(pd.read_sql_query(query_artists, conn))
    
    print("\n--- Top 5 Most Played Tracks ---")
    query_tracks = """
        SELECT t.track_name, t.artist_name, COUNT(l.track_uri) as play_count
        FROM listens l
        JOIN tracks t ON l.track_uri = t.track_uri
        GROUP BY t.track_uri, t.track_name, t.artist_name
        ORDER BY play_count DESC
        LIMIT 5;
    """
    print(pd.read_sql_query(query_tracks, conn))

    print("\n--- Total Listening Time (Hours) ---")
    query_hours = """
        SELECT ROUND(SUM(ms_played) / 1000.0 / 60.0 / 60.0, 2) as total_hours
        FROM listens;
    """
    print(pd.read_sql_query(query_hours, conn))
    
    conn.close()

if __name__ == "__main__":
    run_analytical_queries("spotify_data.db")
