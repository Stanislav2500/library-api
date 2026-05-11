import pytest

class TestAuthors:
    def test_get_authors(self, client):
        response = client.get("/api/authors")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2

    def test_get_author(self, client):
        response = client.get("/api/authors/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "John Doe"

    def test_get_author_not_found(self, client):
        response = client.get("/api/authors/999")
        assert response.status_code == 404

    def test_create_author(self, client):
        response = client.post("/api/authors", json={"name": "New Author"})
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "New Author"

    def test_update_author(self, client):
        response = client.put("/api/authors/1", json={"name": "Updated Name"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Updated Name"

    def test_delete_author(self, client):
        response = client.delete("/api/authors/1")
        assert response.status_code == 204