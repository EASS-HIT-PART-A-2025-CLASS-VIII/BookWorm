from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class BookBase(BaseModel):
    """Shared fields for book creation and reading."""

    title: str
    author: str
    year: int = Field(ge=1400, le=2100)
    genre: str
    pages: int | None = Field(default=None, ge=1)


class Book(BookBase):
    """A book returned from the API - includes server-generated ID."""

    id: int


class BookCreate(BookBase):
    """Incoming payload from the client."""

    @model_validator(mode="after")
    def normalize_fields(self) -> "BookCreate":
        # Normalize author name: "frank herbert" -> "Frank Herbert"
        self.author = " ".join(word.capitalize() for word in self.author.split())

        # Normalize genre: "sci-fi" -> "Sci-Fi"
        self.genre = self.genre.title()

        return self
