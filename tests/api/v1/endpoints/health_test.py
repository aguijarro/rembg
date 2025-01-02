import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_health_db():
    response = client.post("/api/v1/health_db?name=test_item")
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["name"] == "test_item"
