from fastapi.testclient import TestClient
from src.api.main import app, get_db
import sqlite3

# Create an in-memory test database
def override_get_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create minimal schema for testing
    cursor.execute("CREATE TABLE tracks (track_uri TEXT, track_name TEXT, artist_name TEXT)")
    cursor.execute("CREATE TABLE listens (track_uri TEXT, ms_played INTEGER)")
    
    # Insert mock data
    cursor.execute("INSERT INTO tracks VALUES ('uri1', 'Test Song', 'Test Artist')")
    cursor.execute("INSERT INTO listens VALUES ('uri1', 60000)")
    conn.commit()
    
    try:
        yield conn
    finally:
        conn.close()

# Override the database dependency in FastAPI
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health_check():
    """Test the health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is up and running"}

def test_get_top_artists():
    """Test the top-artists endpoint returns the correct structure."""
    response = client.get("/top-artists?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "artist_name" in data[0]
        assert "play_count" in data[0]

def test_get_top_artists_invalid_limit():
    """Test the API correctly rejects an invalid limit query parameter."""
    response = client.get("/top-artists?limit=0")
    assert response.status_code == 422
