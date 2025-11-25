# filepath: tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.dependencies import get_repository


@pytest.fixture(autouse=True)
def clear_repository():
    repo = get_repository()
    repo.clear()
    yield
    repo.clear()


@pytest.fixture
def client():
    return TestClient(app)
