# filepath: tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.dependencies import get_book_service, get_repository
from backend.app.repository import InMemoryBookRepository
from backend.app.service import BookService


@pytest.fixture()
def repo() -> InMemoryBookRepository:
    return InMemoryBookRepository()


@pytest.fixture(autouse=True)
def override_dependencies(repo: InMemoryBookRepository):
    app.dependency_overrides[get_repository] = lambda: repo
    app.dependency_overrides[get_book_service] = lambda: BookService(repo)
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clear_repository(repo: InMemoryBookRepository):
    repo.clear()
    yield
    repo.clear()


@pytest.fixture
def client(override_dependencies):
    return TestClient(app)
