import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_assets" in data
    assert "average_score" in data
    assert data["total_assets"] >= 0

def test_submit_review():
    payload = {"id": 101, "comment": "Great illustration", "rating": 5}
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["received"] == payload

def test_upload_asset():
    new_asset = {
        "id": 3,
        "title": "Jumping Jellyfish",
        "status": "pending",
        "score": 7.5,
        "timestamp": "2023-10-28T10:00:00Z",
        "asset_url": "/assets/jellyfish.png",
        "category": "marine"
    }
    response = client.post("/api/assets/upload", json=new_asset)
    assert response.status_code == 200
    assert response.json()["status"] == "created"
    assert response.json()["id"] == 3