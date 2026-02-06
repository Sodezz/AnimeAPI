# AnimeAPI

Готовый к продакшену FastAPI-сервис для поиска аниме и обогащения данных русскими названиями из внешних источников.

## Что умеет

- Асинхронные API-эндпоинты с валидацией параметров
- Получение популярных аниме и поиск по названию
- Интеграция с AniList (данные о тайтлах)
- Интеграция с Shikimori (русские названия)
- Retry-логика при ошибках внешних API
- Единый стабильный ответ `503`, если upstream недоступен
- In-memory TTL-кэш переводов
- Конфигурация через `.env`
- Запуск через Docker Compose одной командой
- Автотесты сервисного слоя

## Технологический стек

- Python 3.11+
- FastAPI
- HTTPX
- Pydantic v2 + pydantic-settings
- Pytest + pytest-asyncio
- Docker + Docker Compose

## Быстрый старт (рекомендуется)

```bash
cp .env.example .env
docker compose up --build
```

После запуска:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Локальный запуск без Docker

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows PowerShell
pip install -e .[dev]
uvicorn main:app --reload
```

## Переменные окружения

Все переменные и дефолты описаны в `.env.example`.

- `ANILIST_URL` URL AniList GraphQL API
- `SHIKIMORI_URL` URL Shikimori GraphQL API
- `REQUEST_TIMEOUT_SECONDS` таймаут HTTP-запросов
- `MAX_RETRIES` число повторных попыток при ошибках upstream
- `TRANSLATION_CACHE_TTL_SECONDS` TTL кэша переводов в секундах
- `USER_AGENT` User-Agent для внешних запросов
- `AUTH_SHIKIMORI` опциональный заголовок авторизации Shikimori
- `LOG_LEVEL` уровень логирования (`DEBUG`, `INFO`, `WARNING`, `ERROR`)

## API

### `GET /`
Проверка доступности сервиса.

Пример ответа:

```json
{
  "status": "ok",
  "service": "anime-api"
}
```

### `GET /anime/popular?page=1&per_page=10`
Возвращает список популярных аниме.

### `GET /anime?page=1&per_page=10&search=Naruto`
Ищет аниме по названию.

Пример элемента ответа:

```json
{
  "id": 1,
  "english_title": "One Piece",
  "russian_title": "Ван-Пис",
  "average_score": 90
}
```

## Архитектура

- `main.py`: инициализация FastAPI, lifecycle, DI
- `services/fetch_anime_service.py`: работа с AniList
- `services/translate_service.py`: перевод названий через Shikimori + кэш
- `services/catalog_service.py`: orchestration и нормализация ошибок
- `schemas/anime_response.py`: Pydantic-схемы ответа
- `utils/settings.py`: централизованные настройки из `.env`

## Тестирование

```bash
python -m pytest -q
```

## Поведение при сбоях внешних API

Если AniList или Shikimori временно недоступны, сервис возвращает:
- HTTP `503 Service Unavailable`
- сообщение: `Upstream provider is temporarily unavailable`

Это позволяет клиентам обрабатывать такие ошибки единообразно.
