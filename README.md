# URL Shortener API

A modern, production-grade FastAPI URL Shortener and click analytics service.

## Features
- Fully typed FastAPI endpoints.
- SQLite database integration via SQLAlchemy 2.0.
- Unit and integration tests with pytest and in-memory test database.
- Automated GitHub Actions CI pipeline running Ruff linting, formatting checks, pytest coverage, and Docker build.

## Quickstart

```bash
# 1. Install editable package with dev dependencies
pip install -e .[dev]

# 2. Run Ruff format and lint checks
python -m ruff check .
python -m ruff format --check .

# 3. Run test suite with coverage
pytest --cov=url_shortener --cov-report=term-missing --cov-fail-under=85

# 4. Start local development server
uvicorn url_shortener.app:app --reload
```
