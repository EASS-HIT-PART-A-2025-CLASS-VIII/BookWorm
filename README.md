# BookWorm Backend
A clean FastAPI service for managing books, following the architecture from the FastAPI Movie Service exercise (Session 03). Deployed on Render with a PostgreSQL database.

---

## Live API
- Base URL: https://bookworm-api-ad8e.onrender.com
- Health: `GET /health`
- Docs: `https://bookworm-api-ad8e.onrender.com/docs`
- Render uses `DATABASE_URL` for PostgreSQL.

---

## Features
- `GET /health` health check
- `GET /books` list all books
- `POST /books` create a new book
- `GET /books/{id}` get book by ID
- `DELETE /books/{id}` delete a book
- JSON validation with Pydantic
- Repository pattern using SQLModel + PostgreSQL

---

## Project Structure
```bash
BookWorm/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── repository.py
│   ├── backend.Dockerfile
│   └── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Local Development
By default, the app uses SQLite at `bookworm.db`. To use Postgres locally, set `DATABASE_URL=postgresql://user:pass@host:5432/dbname`.

1) Install dependencies (uv)
```bash
uv sync
```

2) Run the server
```bash
uv run uvicorn backend.app.main:app --reload
```

App: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

---

## Running Tests
```bash
uv run pytest -v
```

---

## Running with Docker
1) Build the image
```bash
docker build -t bookworm-backend -f backend.Dockerfile .
```

2) Run the container (set `DATABASE_URL` to use Postgres; otherwise SQLite is used inside the container)
```bash
docker run --rm -p 8000:8000 -e DATABASE_URL=postgresql://user:pass@host:5432/dbname bookworm-backend
```

App: http://127.0.0.1:8000/health

---

## Exporting OpenAPI Schema
Generate `openapi.json` inside `backend/contracts/`:
```bash
uv run python -m backend.scripts.export_openapi
```

---

## Technologies
- Python 3.12
- FastAPI
- SQLModel + PostgreSQL
- Pydantic
- Pytest
- Docker
- uv package manager

---

## Purpose
Learning exercise from Session 03 (FastAPI Fundamentals). The BookWorm theme replaces movies with books while keeping the same architecture.

---

## License
Free for educational and personal use.
