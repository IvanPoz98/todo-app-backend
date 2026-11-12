# Todo API

Async REST API для задач на **FastAPI + PostgreSQL + SQLAlchemy 2.0 + Alembic**.

Проект сделан со слоистой архитектурой.

## Стек

- Python 3.12+
- FastAPI
- PostgreSQL 16
- SQLAlchemy 2.0 (AsyncSession)
- Alembic
- Docker Compose
- Pydantic v2 / pydantic-settings

## Архитектура

```text
HTTP request
  → api/routers      (валидация, HTTP)
  → Depends          (сессия + сервис)
  → services         (бизнес-логика, commit)
  → repositories     (работа с БД)
  → PostgreSQL
```

## Структура

```text
app/
  api/           # routers, dependencies
  core/          # settings
  db/            # engine, session
  models/        # SQLAlchemy ORM
  repositories/  # data access
  schemas/       # Pydantic schemas
  services/      # business logic
  main.py
alembic/         # migrations
docker-compose.yml
```

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/IvanPoz98/todo-app-backend.git
cd todo-app-backend
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Git Bash
source .venv/Scripts/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
pip install asyncpg alembic sqlalchemy pydantic-settings
```

### 4. Настроить окружение

```bash
cp .env.example app/.env
```

При необходимости поправь значения в `app/.env`.

### 5. Поднять Postgres

```bash
docker compose up -d
```

База будет на `localhost:5439`.

### 6. Применить миграции

```bash
alembic upgrade head
```

### 7. Запустить API

```bash
uvicorn app.main:app --reload
```

- Swagger: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

## API

| Метод | URL | Описание |
|------|-----|----------|
| GET | `/tasks` | Список задач |
| POST | `/tasks` | Создать задачу |
| PATCH | `/tasks/{id}` | Обновить задачу |
| DELETE | `/tasks/{id}` | Удалить задачу |

Пример создания:

```json
{
  "title": "Изучить FastAPI",
  "description": "Слои, Depends, async SQLAlchemy"
}
```

## Миграции

Изменение схемы БД только через Alembic:

```bash
alembic revision --autogenerate -m "short message"
alembic upgrade head
```

## Git-процесс

Работа идёт через feature-ветки и Pull Request в `main`:

```bash
git checkout main
git pull
git checkout -b feature/my-change
# ...code...
git add .
git commit -m "meaningful message"
git push -u origin feature/my-change
gh pr create
```
