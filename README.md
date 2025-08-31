# Bonus System — тестовое задание

В проекте реализована система уровней для игроков с получения призов и выгрузку данных в csv-формате

---

## Установка

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/base.txt

```

## Назначение

Сервис:

- хранит игроков, уровни и призы;
- фиксирует прохождение уровня игроком;
- выдаёт приз за уровень;
- выгружает прогресс в CSV.

## Стек

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x (async) + `asyncpg`
- Alembic (миграции через `psycopg2`)
- PostgreSQL 16
- Docker
- Ruff + pre-commit (линт и форматирование)

## Структура проекта

```text
apps/
├─ bonus_system/
│  ├─ route.py          # эндпоинты FastAPI (выдача приза за прохождение, экспорт CSV)
│  ├─ schemas.py        # Pydantic-схемы запросов/ответов
│  └─ services.py       # бизнес-логика (level_is_passed, экспорт)
└─ core/
   ├─ bootstraps/       # инициализация приложения
   ├─ dependencies/     # Depends
   ├─ exceptions/       # общие исключения
   ├─ models/
   │  └─ task-1/ 
          |─ models.py  # Хранится 1 задача (модели)
│     ├─ base.py        # Base / общие поля
│     ├─ player.py      # Player, PlayerLevel, PlayerHistory
│     ├─ level.py       # Level, LevelPrize
│     └─ prize.py       # Prize
   ├─ config.py         # настройки (в т.ч. DATABASE_URL)
   ├─ database.py       # движок/сессия (async)
   ├─ enums.py
   └─ router.py         # сборка маршрутов /api/v1/...
migrations/             # Alembic-миграции
ruff/                   # линт/формат
.env
.pre-commit-config.yaml
README.md
DockerFile
docker-compose.yml