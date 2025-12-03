# filepath: backend/app/main.py
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status, HTTPException

from .db import init_db
from .dependencies import SettingsDep, ServiceDep
from .models import Book, BookCreate
from .types import BookNotFoundError

logger = logging.getLogger("backend")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    init_db()
    yield


app = FastAPI(title="BookWorm API", version="0.3.0", lifespan=lifespan)


@app.get("/health")
def health(settings: SettingsDep) -> dict[str, str]:
    """Health check endpoint with app name from Settings."""
    return {"status": "ok", "app": settings.app_name}


@app.get("/books", response_model=list[Book])
def list_books(service: ServiceDep) -> list[Book]:
    """Return all books."""
    return service.list_all()


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, service: ServiceDep) -> Book:
    """Create a new book."""
    book = service.create_book(payload)
    logger.info("book.created id=%s title=%s", book.id, book.title)
    return book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, service: ServiceDep) -> Book:
    """Retrieve a single book by ID."""
    try:
        return service.get_book(book_id)
    except BookNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        ) from exc


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, service: ServiceDep) -> None:
    """Delete a book by ID."""
    try:
        service.delete_book(book_id)
    except BookNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        ) from exc
    logger.info("book.deleted id=%s", book_id)
