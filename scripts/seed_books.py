# filepath: backend/scripts/seed_books.py
from sqlmodel import Session
from backend.app.db import engine, init_db, BookTable
from backend.app.models import BookCreate
import json
import pathlib


def load_books() -> list[BookCreate]:
    """Load books.json file located next to this script."""
    path = pathlib.Path(__file__).parent / "books.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [BookCreate(**item) for item in data]


def seed() -> None:
    init_db()
    books = load_books()

    print(f"Seeding {len(books)} books...")

    with Session(engine) as session:
        for book in books:
            row = BookTable(
                title=book.title,
                author=book.author,
                year=book.year,
                genre=book.genre,
                pages=book.pages,
            )
            session.add(row)
        session.commit()

    print("Done!")


if __name__ == "__main__":
    seed()
