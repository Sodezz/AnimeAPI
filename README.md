**AnimeAPI** — API для поиска и получения информации об аниме с переводом на русский язык и средней оценкой.

---

# Описание проекта

AnimeAPI предоставляет **возможности**:

- Поиска аниме по названию (английский → русский перевод)

- Получения списка популярных аниме

- Включает информацию о средней оценке (average score)

- API интегрируется с AniList (для данных о тайтлах) и Shikimori GraphQL API (для перевода).

---

# Установка

Выполнить скрипт:

```bash
git clone https://github.com/Sodezz/AnimeAPI.git

cd AnimeAPI

python3 -m venv venv

source venv/bin/activate  # или venv\Scripts\activate на Windows

pip install -r requirements.txt

uvicorn main:app --reload
```

Заполнить файл `.env`:

```ini
USERAGENT=твой-user-agent
AUTHSHIKIMORI=твой-токен-Shikimori
```

---

# Использование

## Пример: популярные аниме

Запрос:

```bash
GET /anime/popular?page=1&per_page=3

```

Ответ:

```json
[
  {
    "russian_title": "Атака титанов",
    "average_score": 84
  },
  {
    "russian_title": "Клинок, рассекающий демонов",
    "average_score": 82
  },
  {
    "russian_title": "Тетрадь смерти",
    "average_score": 84
  }
]

```

## Пример: поиск по названию

Запрос:

```bash
GET /anime/?search=Naruto&page=1&per_page=2
```

Ответ:

```json
[
  {
    "russian_title": "Наруто",
    "average_score": 78
  },
  {
    "russian_title": "Наруто: Ураганные хроники",
    "average_score": 79
  }
]

```


---

# Функции

- Поиск аниме по английскому названию с переводом на русский

- Вывод среднего балла (averageScore)

- Пагинация (page, per_page)

- Типизация Pydantic и OpenAPI документация Swagger UI
