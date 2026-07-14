"""
Tests for the FastAPI application
Tests the main endpoints and error handling
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealth:
    """Health check endpoint tests"""

    def test_health_check_returns_ok(self):
        """Test that health check returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data


class TestItems:
    """Items endpoint tests"""

    def test_list_items_empty(self):
        """Test listing items when database is empty"""
        response = client.get("/api/items")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_item(self):
        """Test creating a new item"""
        item_data = {"title": "Test Item", "description": "This is a test item", "completed": False}
        response = client.post("/api/items", json=item_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == item_data["title"]
        assert data["description"] == item_data["description"]
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_create_item_minimal(self):
        """Test creating item with only required fields"""
        item_data = {"title": "Minimal Item"}
        response = client.post("/api/items", json=item_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Item"
        assert data["description"] is None

    def test_create_item_missing_title(self):
        """Test creating item without title fails"""
        item_data = {"description": "No title"}
        response = client.post("/api/items", json=item_data)
        assert response.status_code == 422  # Validation error

    def test_get_item(self):
        """Test retrieving a specific item"""
        # First create an item
        item_data = {"title": "Get Me"}
        create_response = client.post("/api/items", json=item_data)
        item_id = create_response.json()["id"]

        # Then get it
        response = client.get(f"/api/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["title"] == "Get Me"

    def test_get_item_not_found(self):
        """Test getting non-existent item returns 404"""
        response = client.get("/api/items/99999")
        assert response.status_code == 404

    def test_update_item(self):
        """Test updating an item"""
        # Create item
        item_data = {"title": "Original", "completed": False}
        create_response = client.post("/api/items", json=item_data)
        item_id = create_response.json()["id"]

        # Update it
        updated_data = {"title": "Updated", "completed": True}
        response = client.put(f"/api/items/{item_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["completed"] is True

    def test_delete_item(self):
        """Test deleting an item"""
        # Create item
        item_data = {"title": "Delete Me"}
        create_response = client.post("/api/items", json=item_data)
        item_id = create_response.json()["id"]

        # Delete it
        response = client.delete(f"/api/items/{item_id}")
        assert response.status_code == 204

        # Verify it's gone
        response = client.get(f"/api/items/{item_id}")
        assert response.status_code == 404

    def test_delete_item_not_found(self):
        """Test deleting non-existent item returns 404"""
        response = client.delete("/api/items/99999")
        assert response.status_code == 404
