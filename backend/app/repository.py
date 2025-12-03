# filepath: backend/app/repository.py
from __future__ import annotations

from typing import Dict

from sqlmodel import Session, select, delete

from .db import engine, BookTable
from .models import Book, BookCreate


class InMemoryBookRepository:
    """Existing in-memory repository (still useful for reference or fallback)."""

    def __init__(self) -> None:
        self._items: Dict[int, Book] = {}
        self._next_id = 1

    def list(self) -> list[Book]:
        return list(self._items.values())

    def create(self, payload: BookCreate) -> Book:
        book = Book(id=self._next_id, **payload.model_dump())
        self._items[book.id] = book
        self._next_id += 1
        return book

    def create_many(self, payloads: list[BookCreate]) -> list[Book]:
        created: list[Book] = []
        for payload in payloads:
            created.append(self.create(payload))
        return created

    def get(self, book_id: int) -> Book | None:
        return self._items.get(book_id)

    def delete(self, book_id: int) -> None:
        self._items.pop(book_id, None)

    def clear(self) -> None:
        self._items.clear()
        self._next_id = 1


class DbBookRepository:
    """PostgreSQL/SQLModel-backed repository."""

    def list(self) -> list[Book]:
        with Session(engine) as session:
            rows = session.exec(select(BookTable)).all()
            return [self._to_book(row) for row in rows]

    def create(self, payload: BookCreate) -> Book:
        with Session(engine) as session:
            db_book = BookTable(**payload.model_dump())
            session.add(db_book)
            session.commit()
            session.refresh(db_book)
            return self._to_book(db_book)

    def create_many(self, payloads: list[BookCreate]) -> list[Book]:
        created: list[Book] = []
        with Session(engine) as session:
            for payload in payloads:
                db_book = BookTable(**payload.model_dump())
                session.add(db_book)
                session.flush()  # get ids without committing each loop
                session.refresh(db_book)
                created.append(self._to_book(db_book))
            session.commit()
        return created

    def get(self, book_id: int) -> Book | None:
        with Session(engine) as session:
            db_book = session.get(BookTable, book_id)
            if not db_book:
                return None
            return self._to_book(db_book)

    def delete(self, book_id: int) -> None:
        with Session(engine) as session:
            db_book = session.get(BookTable, book_id)
            if not db_book:
                return
            session.delete(db_book)
            session.commit()

    def clear(self) -> None:
        """Clear all books (used by tests to isolate state)."""
        with Session(engine) as session:
            session.exec(delete(BookTable))
            session.commit()

    @staticmethod
    def _to_book(db_book: BookTable) -> Book:
        return Book(
            id=db_book.id,
            title=db_book.title,
            author=db_book.author,
            year=db_book.year,
            genre=db_book.genre,
            pages=db_book.pages,
        )
