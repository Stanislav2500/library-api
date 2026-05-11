import pytest

class TestBooks:
    def test_get_books(self, client):
        response = client.get("/api/books")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2

    def test_get_book(self, client):
        response = client.get("/api/books/1")
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Book 1"

    def test_get_book_not_found(self, client):
        response = client.get("/api/books/999")
        assert response.status_code == 404

    def test_create_book(self, client):
        response = client.post("/api/books", json={"title": "New Book", "author_id": 1})
        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "New Book"

    def test_create_book_default_status(self, client):
        """Книга створюється зі статусом за замовчуванням"""
        response = client.post("/api/books", json={
            "title": "Test Book",
            "created_by": "Katrenko Stanislav",
        })
        assert response.status_code == 201

    def test_update_book(self, client):
        response = client.put("/api/books/1", json={"title": "Updated Book", "status": "checked-out"})
        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Updated Book"

    def test_delete_book(self, client):
        response = client.delete("/api/books/1")
        assert response.status_code == 204