from fastapi.testclient import TestClient
from src.api.main import app

# Create a TestClient instance passing our FastAPI app
client = TestClient(app)

def test_health_check():
    """Test the health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API is up and running"}

def test_get_top_artists():
    """Test the top-artists endpoint returns the correct structure and respects the limit."""
    response = client.get("/top-artists?limit=2")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 2  # It should respect our limit=2
    
    if len(data) > 0:
        assert "artist_name" in data[0]
        assert "play_count" in data[0]

def test_get_top_artists_invalid_limit():
    """Test the API correctly rejects an invalid limit query parameter."""
    # Our API requires limit >= 1. Sending 0 should trigger a 422 Validation Error.
    response = client.get("/top-artists?limit=0")
    assert response.status_code == 422
