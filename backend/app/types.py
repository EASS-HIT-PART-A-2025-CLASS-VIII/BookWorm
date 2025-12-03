"""Domain-level shared types and errors."""

from typing import Protocol

from .models import Book, BookCreate


class BookRepository(Protocol):
    def list(self) -> list[Book]: ...

    def create(self, payload: BookCreate) -> Book: ...

    def get(self, book_id: int) -> Book | None: ...

    def delete(self, book_id: int) -> None: ...


class BookNotFoundError(Exception):
    """Raised when a book cannot be located."""
