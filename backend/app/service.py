"""Business logic layer for book operations."""

from __future__ import annotations

from .models import Book, BookCreate
from .types import BookNotFoundError, BookRepository


class BookService:
    """Service layer that encapsulates business logic for books."""

    def __init__(self, repository: BookRepository) -> None:
        self.repository = repository

    def list_all(self) -> list[Book]:
        """Retrieve all books."""
        return self.repository.list()

    def create_book(self, payload: BookCreate) -> Book:
        """Create a new book and persist to database."""
        return self.repository.create(payload)

    def get_book(self, book_id: int) -> Book:
        """Retrieve a single book by ID. Raises 404 if not found."""
        book = self.repository.get(book_id)
        if not book:
            raise BookNotFoundError(f"id={book_id}")
        return book

    def delete_book(self, book_id: int) -> None:
        """Delete a book by ID. Raises 404 if not found."""
        book = self.repository.get(book_id)
        if not book:
            raise BookNotFoundError(f"id={book_id}")
        self.repository.delete(book_id)
