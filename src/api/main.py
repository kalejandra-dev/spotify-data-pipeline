from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI(
    title="Spotify Data API",
    description="API to query personal Spotify listening history.",
    version="1.0.0"
)

DB_PATH = "spotify_data.db"

# --- Pydantic Response Models ---
class TopArtistResponse(BaseModel):
    artist_name: str
    play_count: int

class TopTrackResponse(BaseModel):
    track_name: str
    artist_name: str
    play_count: int

class ListeningStatsResponse(BaseModel):
    total_hours: float
    unique_tracks: int

def get_db():
    """Dependency function to get a database connection per request."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    try:
        yield conn
    finally:
        conn.close()

@app.get("/health", tags=["System"])
def health_check():
    """Checks if the API is running correctly."""
    return {"status": "ok", "message": "API is up and running"}

@app.get("/top-artists", response_model=List[TopArtistResponse], tags=["Analytics"])
def get_top_artists(
    limit: int = Query(5, ge=1, le=50, description="Number of artists to return"),
    db: sqlite3.Connection = Depends(get_db)
):
    """Returns the most played artists based on play count."""
    cursor = db.cursor()
    query = """
        SELECT t.artist_name, COUNT(l.track_uri) as play_count
        FROM listens l
        JOIN tracks t ON l.track_uri = t.track_uri
        GROUP BY t.artist_name
        ORDER BY play_count DESC
        LIMIT ?
    """
    cursor.execute(query, (limit,))
    return [dict(row) for row in cursor.fetchall()]

@app.get("/top-tracks", response_model=List[TopTrackResponse], tags=["Analytics"])
def get_top_tracks(
    limit: int = Query(5, ge=1, le=50, description="Number of tracks to return"),
    db: sqlite3.Connection = Depends(get_db)
):
    """Returns the most played tracks based on play count."""
    cursor = db.cursor()
    query = """
        SELECT t.track_name, t.artist_name, COUNT(l.track_uri) as play_count
        FROM listens l
        JOIN tracks t ON l.track_uri = t.track_uri
        GROUP BY t.track_uri, t.track_name, t.artist_name
        ORDER BY play_count DESC
        LIMIT ?
    """
    cursor.execute(query, (limit,))
    return [dict(row) for row in cursor.fetchall()]

@app.get("/listening-stats", response_model=ListeningStatsResponse, tags=["Analytics"])
def get_listening_stats(db: sqlite3.Connection = Depends(get_db)):
    """Returns overall listening statistics (total hours and unique tracks)."""
    cursor = db.cursor()
    query = """
        SELECT 
            ROUND(SUM(ms_played) / 1000.0 / 60.0 / 60.0, 2) as total_hours,
            COUNT(DISTINCT track_uri) as unique_tracks
        FROM listens
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return dict(row)
