# filepath: backend/app/dependencies.py
from typing import Annotated

from fastapi import Depends

from .config import Settings
from .repository import BookRepository

# Single instances shared across requests
_settings = Settings()
_repository = BookRepository()


def get_settings() -> Settings:
    """Provide Settings to endpoints."""
    return _settings


def get_repository() -> BookRepository:
    """Provide BookRepository to endpoints."""
    return _repository


# Type aliases for cleaner endpoint signatures
SettingsDep = Annotated[Settings, Depends(get_settings)]
RepositoryDep = Annotated[BookRepository, Depends(get_repository)]
