# BookWorm Backend
FastAPI service for managing books, deployed on Render with PostgreSQL.

---

## :globe_with_meridians: Live API on Render
- Base URL: https://bookworm-api-ad8e.onrender.com
- Health: `GET /health`
- Docs: `https://bookworm-api-ad8e.onrender.com/docs`
- Render uses `DATABASE_URL` for PostgreSQL.

---

## :sparkles: Features
- `GET /health` health check
- `GET /books` list all books
- `POST /books` create a new book
- `GET /books/{id}` get book by ID
- `DELETE /books/{id}` delete a book
- JSON validation with Pydantic
- Repository pattern using SQLModel + PostgreSQL

---

## :card_file_box: Project Structure
```bash
BookWorm/
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- models.py
|   |   |-- config.py
|   |   |-- dependencies.py
|   |   `-- repository.py
|   |-- backend.Dockerfile
|   `-- tests/
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

---

## :hammer_and_wrench: Local Development
- Default DB: SQLite at `bookworm.db`.
- To use Postgres locally: set `DATABASE_URL=postgresql://user:pass@host:5432/dbname` (replace `host` with a reachable host like `localhost`).

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

## :test_tube: Running Tests
```bash
uv run pytest -v
```

---

## :whale: Running with Docker
1) Build the image
```bash
docker build -t bookworm-backend -f backend.Dockerfile .
```

2) Run the container (uses SQLite by default; optionally set `DATABASE_URL` to point at Postgres)
```bash
docker run --rm -p 8000:8000 bookworm-backend
```

App: http://127.0.0.1:8000/health

---

## :bookmark_tabs: Exporting OpenAPI Schema
Generate `openapi.json` inside `backend/contracts/`:
```bash
uv run python -m backend.scripts.export_openapi
```

---

## :toolbox: Technologies
- Python 3.12
- FastAPI
- SQLModel + PostgreSQL
- Pydantic
- Pytest
- Docker
- uv package manager

---

## :dart: Purpose
Learning exercise from Session 03 (FastAPI Fundamentals). The BookWorm theme replaces movies with books while keeping the same architecture.

---

## :scroll: License
Free for educational and personal use.
