# filepath: backend/app/dependencies.py
from typing import Annotated

from fastapi import Depends

from .config import Settings
from .repository import DbBookRepository


_settings = Settings()
_repository = DbBookRepository()


def get_settings() -> Settings:
    return _settings


def get_repository() -> DbBookRepository:
    return _repository


SettingsDep = Annotated[Settings, Depends(get_settings)]
RepositoryDep = Annotated[DbBookRepository, Depends(get_repository)]
