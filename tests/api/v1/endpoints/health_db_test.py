import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from datetime import datetime
from unittest.mock import patch
from app.main import app
from app.core.mongodb import mongodb
from mongomock_motor import AsyncMongoMockClient

# Mock data for health tests
MOCK_STORED_ITEMS = [
    {
        "_id": "123456789",
        "name": "test_item_1",
        "created_at": datetime.utcnow()
    },
    {
        "_id": "987654321",
        "name": "test_item_2",
        "created_at": datetime.utcnow()
    }
]

@pytest.fixture
def test_app():
    return TestClient(app)

@pytest.fixture
async def async_client():
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    await client.aclose()

@pytest.fixture(autouse=True)
async def mock_db():
    """Setup mock MongoDB for testing"""
    mock_client = AsyncMongoMockClient()
    mock_db = mock_client['test_db']
    mongodb.client = mock_client
    mongodb.db = mock_db
    yield mock_db
    mongodb.client = None
    mongodb.db = None

@pytest.mark.asyncio
async def test_get_all_items_success(test_app, mock_db):
    """Test successful retrieval of all stored items"""
    with patch('app.repositories.health_repository.HealthRepository.get_all_items') as mock_get:
        mock_response = []
        for doc in MOCK_STORED_ITEMS:
            doc_copy = doc.copy()
            doc_copy['id'] = str(doc_copy.pop('_id'))
            mock_response.append(doc_copy)
        
        mock_get.return_value = mock_response
        response = test_app.get("/api/v1/health_db")
        
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["name"] == "test_item_1"
        assert response.json()[1]["name"] == "test_item_2"
        assert "id" in response.json()[0]
        assert "created_at" in response.json()[0]
        mock_get.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_items_empty(test_app, mock_db):
    """Test retrieval when no items are stored"""
    with patch('app.repositories.health_repository.HealthRepository.get_all_items') as mock_get:
        mock_get.return_value = []
        response = test_app.get("/api/v1/health_db")
        
        assert response.status_code == 200
        assert response.json() == []
        mock_get.assert_called_once()

@pytest.mark.asyncio
async def test_create_item_success(test_app, mock_db):
    """Test successful creation of an item"""
    mock_item = {
        "_id": "test123",
        "name": "test_item",
        "created_at": datetime.utcnow()
    }
    
    with patch('app.repositories.health_repository.HealthRepository.create_item') as mock_create:
        mock_create.return_value = mock_item
        response = test_app.post("/api/v1/health_db", params={"name": "test_item"})
        
        assert response.status_code == 200
        result = response.json()
        assert result["name"] == "test_item"
        assert "_id" in result
        assert "created_at" in result
        mock_create.assert_called_once_with("test_item")

@pytest.mark.asyncio
async def test_create_item_with_query_param(test_app, mock_db):
    """Test creating item using query parameter"""
    mock_item = {
        "_id": "test123",
        "name": "test_item",
        "created_at": datetime.utcnow()
    }
    
    with patch('app.repositories.health_repository.HealthRepository.create_item') as mock_create:
        mock_create.return_value = mock_item
        response = test_app.post("/api/v1/health_db?name=test_item")
        
        assert response.status_code == 200
        result = response.json()
        assert result["name"] == "test_item"
        assert "_id" in result
        assert "created_at" in result
        mock_create.assert_called_once_with("test_item")