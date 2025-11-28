# filepath: backend/app/db.py
from __future__ import annotations

import os
from typing import Generator

from sqlmodel import SQLModel, Field, create_engine, Session


# Use DATABASE_URL if set (e.g. on Render with Postgres),
# otherwise fall back to a local SQLite file for development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bookworm.db")

# echo=True logs SQL queries; handy for debugging locally.
engine = create_engine(DATABASE_URL, echo=False)


class BookTable(SQLModel, table=True):
    __tablename__ = "books"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int
    genre: str
    pages: int | None = None


def init_db() -> None:
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a SQLModel Session (for DI if we need it later)."""
    with Session(engine) as session:
        yield session
