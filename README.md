

# 📚 BookWorm Backend  
A clean FastAPI service for managing books — built for learning modern backend development, following the same architecture used in the FastAPI Movie Service exercise (Session 03).

This project includes:

- FastAPI application  
- Book CRUD API  
- Pydantic models & validation  
- Repository + Dependency Injection  
- Pytest test suite  
- Docker image  
- OpenAPI export  
- Optional seed script for large book datasets  

---

## 🚀 Features

- `GET /health` – health check  
- `GET /books` – list all books  
- `POST /books` – create a new book  
- `GET /books/{id}` – get book by ID  
- `DELETE /books/{id}` – delete a book  
- `POST /books/bulk` – create multiple books at once  
- JSON validation using Pydantic  
- Repository pattern for testability  
- Dependency injection with FastAPI `Depends`  

---

## 📁 Project Structure


```bash
BookWorm/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── repository.py
│   └── scripts/
│       ├── seed_books.py
│       └── export_openapi.py
│
├── backend.Dockerfile
├── tests/
│   ├── conftest.py
│   └── test_books.py
├── data/
│   └── books_seed.json
├── pyproject.toml
├── uv.lock
└── README.md
```


---

## 🛠️ Setup (Local Development)

### 1. Install dependencies (using uv)

```bash
uv sync
````

### 2. Run the server

```bash
uv run uvicorn backend.app.main:app --reload
```

App will be available at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Running Tests

The project includes a complete pytest test suite.

Run all tests:

```bash
uv run pytest -v
```

---

## 🐳 Running with Docker

### 1. Build the image

```bash
docker build -t bookworm-backend -f backend.Dockerfile .
```

### 2. Run the container

```bash
docker run --rm -p 8000:8000 bookworm-backend
```

Then open:

```
http://127.0.0.1:8000/health
```

---

## 📤 Exporting OpenAPI Schema

Generate `openapi.json` inside `backend/contracts/`:

```bash
uv run python -m backend.scripts.export_openapi
```

---

## 🌱 Seeding Data (Optional)

This project includes an optional seed script that loads a JSON list of books.

Example usage:

```bash
uv run python -m backend.scripts.seed_books data/books_seed.json --clear
```

This is **not required** for the assignment — just a convenient development tool.

---

## 📘 Example Book Payload

```json
{
  "title": "Dune",
  "author": "Frank Herbert",
  "year": 1965,
  "genre": "Sci-Fi",
  "pages": 412
}
```

---

## 📚 Bulk Insert Example

Send an array of books to:

`POST /books/bulk`

```json
[
  {
    "title": "Dune",
    "author": "Frank Herbert",
    "year": 1965,
    "genre": "Sci-Fi",
    "pages": 412
  },
  {
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "year": 1937,
    "genre": "Fantasy",
    "pages": 310
  }
]
```

---

## 🧩 Technologies

* Python 3.12
* FastAPI
* Pydantic
* Pytest
* Docker
* uv package manager

---

## 🎓 Purpose

This project was built as a learning exercise, following the patterns taught in Session 03 (FastAPI Fundamentals).
The “BookWorm” theme replaces movies with books, but follows all the same architectural patterns:

* Repository abstraction
* Dependency injection
* Pydantic models
* Clear file structure
* Tests using TestClient

---

## 📝 License

Free for educational and personal use.



