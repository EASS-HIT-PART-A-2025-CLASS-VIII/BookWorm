# filepath: tests/test_books.py
"""
Test suite for BookWorm API.
"""

# The `client` fixture comes from conftest.py – pytest injects it automatically.


def test_health_includes_app_name(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    # Default app name (from Settings defaults or .env)
    assert "BookWorm" in data["app"]


def test_create_book_returns_201_and_payload(client):
    response = client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "frank herbert",
            "year": 1965,
            "genre": "sci-fi",
            "pages": 412,
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Dune"
    assert data["year"] == 1965
    assert data["pages"] == 412

    # Normalization checks
    assert data["author"] == "Frank Herbert"
    assert data["genre"] == "Sci-Fi"

    # ID should be generated
    assert data["id"] == 1


def test_book_ids_increment(client):
    first = client.post(
        "/books",
        json={
            "title": "Book One",
            "author": "author one",
            "year": 2000,
            "genre": "fantasy",
            "pages": 123,
        },
    ).json()["id"]

    second = client.post(
        "/books",
        json={
            "title": "Book Two",
            "author": "author two",
            "year": 2001,
            "genre": "fantasy",
            "pages": 222,
        },
    ).json()["id"]

    assert second == first + 1


def test_list_books_initially_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []


def test_list_books_after_creation(client):
    client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "frank herbert",
            "year": 1965,
            "genre": "sci-fi",
            "pages": 412,
        },
    )

    response = client.get("/books")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 1
    assert books[0]["title"] == "Dune"


def test_get_book_by_id(client):
    create_response = client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "frank herbert",
            "year": 1965,
            "genre": "sci-fi",
            "pages": 412,
        },
    )
    book_id = create_response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    book = response.json()
    assert book["id"] == book_id
    assert book["title"] == "Dune"


def test_get_missing_book_returns_404(client):
    response = client.get("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_delete_book(client):
    create_response = client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "frank herbert",
            "year": 1965,
            "genre": "sci-fi",
            "pages": 412,
        },
    )
    book_id = create_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


def test_delete_missing_book_returns_404(client):
    response = client.delete("/books/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"


def test_create_book_rejects_year_too_old(client):
    response = client.post(
        "/books",
        json={
            "title": "Ancient Book",
            "author": "old author",
            "year": 1000,  # too old (< 1400)
            "genre": "history",
            "pages": 10,
        },
    )
    assert response.status_code == 422  # validation error


def test_create_book_rejects_year_too_new(client):
    response = client.post(
        "/books",
        json={
            "title": "Future Book",
            "author": "future author",
            "year": 2500,  # > 2100
            "genre": "sci-fi",
            "pages": 200,
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_missing_title(client):
    response = client.post(
        "/books",
        json={
            "author": "someone",
            "year": 2020,
            "genre": "drama",
            "pages": 100,
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_missing_author(client):
    response = client.post(
        "/books",
        json={
            "title": "No Author",
            "year": 2020,
            "genre": "drama",
            "pages": 100,
        },
    )
    assert response.status_code == 422


def test_create_book_rejects_invalid_pages(client):
    response = client.post(
        "/books",
        json={
            "title": "Zero Pages",
            "author": "whoever",
            "year": 2020,
            "genre": "drama",
            "pages": 0,
        },
    )
    assert response.status_code == 422
