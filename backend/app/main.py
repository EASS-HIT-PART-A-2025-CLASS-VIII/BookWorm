# filepath: backend/app/main.py
from __future__ import annotations

from .db import init_db

import logging

from fastapi import FastAPI, HTTPException, status

from .dependencies import SettingsDep, RepositoryDep
from .models import Book, BookCreate

logger = logging.getLogger("backend")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

app = FastAPI(title="BookWorm API", version="0.3.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()



@app.get("/health")
def health(settings: SettingsDep) -> dict[str, str]:
    """Health check endpoint with app name from Settings."""
    return {"status": "ok", "app": settings.app_name}


@app.get("/books", response_model=list[Book])
def list_books(repo: RepositoryDep) -> list[Book]:
    """Return all books."""
    return repo.list()


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, repo: RepositoryDep) -> Book:
    """Create a new book."""
    book = repo.create(payload)
    logger.info("book.created id=%s title=%s", book.id, book.title)
    return book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, repo: RepositoryDep) -> Book:
    """Retrieve a single book by ID."""
    book = repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, repo: RepositoryDep) -> None:
    """Delete a book by ID."""
    if not repo.get(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    repo.delete(book_id)
    logger.info("book.deleted id=%s", book_id)

