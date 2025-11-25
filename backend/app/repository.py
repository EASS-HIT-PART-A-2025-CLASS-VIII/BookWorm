# filepath: backend/app/repository.py
from __future__ import annotations

from typing import Dict

from .models import Book, BookCreate


class BookRepository:
    """In-memory storage for books.

    Later you can replace this with a DB (SQLModel, Postgres, etc.)
    without changing the endpoints, only this class.
    """

    def __init__(self) -> None:
        self._items: Dict[int, Book] = {}
        self._next_id = 1

    def list(self) -> list[Book]:
        """Return all books."""
        return list(self._items.values())

    def create(self, payload: BookCreate) -> Book:
        """Create a new book and return it."""
        book = Book(id=self._next_id, **payload.model_dump())
        self._items[book.id] = book
        self._next_id += 1
        return book

    def get(self, book_id: int) -> Book | None:
        """Get book by ID, or None if not found."""
        return self._items.get(book_id)

    def delete(self, book_id: int) -> None:
        """Delete a book by ID, no error if missing."""
        self._items.pop(book_id, None)

    def clear(self) -> None:
        """Reset storage (useful for tests)."""
        self._items.clear()
        self._next_id = 1