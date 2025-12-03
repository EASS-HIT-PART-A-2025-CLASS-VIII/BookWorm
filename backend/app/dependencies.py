# filepath: backend/app/dependencies.py
from typing import Annotated

from fastapi import Depends

from .config import Settings
from .repository import DbBookRepository
from .service import BookService


_settings = Settings()
_repository = DbBookRepository()
_service = BookService(_repository)


def get_settings() -> Settings:
    return _settings


def get_repository() -> DbBookRepository:
    return _repository


def get_book_service() -> BookService:
    return _service


SettingsDep = Annotated[Settings, Depends(get_settings)]
RepositoryDep = Annotated[DbBookRepository, Depends(get_repository)]
ServiceDep = Annotated[BookService, Depends(get_book_service)]
