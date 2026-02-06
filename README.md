# AnimeAPI

Production-ready FastAPI service for anime discovery with Russian title enrichment from external providers.

## Features

- Async API with typed responses and validated query params
- Popular anime endpoint and search endpoint
- AniList integration with retry logic and stable 503 fallback
- Shikimori title translation with in-memory TTL cache
- Environment-driven config via `.env`
- Dockerized one-command startup
- Unit tests for service layer

## Tech Stack

- Python 3.11
- FastAPI
- HTTPX
- Pydantic v2 + pydantic-settings
- Pytest
- Docker + Docker Compose

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

App: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

## Local Run

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -e .[dev]
uvicorn main:app --reload
```

## Environment Variables

See `.env.example`.

- `USER_AGENT` custom user agent for upstream requests
- `AUTH_SHIKIMORI` optional Shikimori authorization header value
- `REQUEST_TIMEOUT_SECONDS` request timeout
- `MAX_RETRIES` upstream retry attempts
- `TRANSLATION_CACHE_TTL_SECONDS` translation cache TTL
- `LOG_LEVEL` logging level

## API

- `GET /` health check
- `GET /anime/popular?page=1&per_page=10`
- `GET /anime?page=1&per_page=10&search=Naruto`

## Testing

```bash
pytest -q
```
