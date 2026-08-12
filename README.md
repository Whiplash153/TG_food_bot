# TG Food Bot

A portfolio MVP Telegram bot for a company that provides food storage services.

The bot helps users quickly get basic company information, view active promotions, and submit a contact request. Each request is saved to PostgreSQL, then the manager receives a Telegram notification.

## Status

The project is completed as an L1 / portfolio MVP. The next iteration with promotion filtering and additional domain entities is intentionally not implemented. The goal of this version is to show a finished, small, understandable Telegram bot with clear layer separation.

## Features

- `/start` creates or updates a user by Telegram ID;
- main menu is available through a persistent Telegram keyboard;
- sections: promotions, company info, FAQ, contacts;
- promotions are stored in PostgreSQL and displayed only when active;
- contact requests are submitted through a step-by-step form;
- required request fields: name and phone;
- city, company, email, and comment are optional;
- phone and email have basic validation;
- unfinished requests are not saved to the database;
- completed requests are saved to PostgreSQL;
- the manager receives a Telegram notification;
- the user receives confirmation after the request is saved;
- if the manager notification fails, the request remains in the database with `failed` status.

## Tech Stack

- Python 3.12
- python-telegram-bot
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Docker Compose
- Pydantic Settings
- Poetry

## Architecture

The project is split into several layers:

```text
Telegram Update
    ↓
Handler
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy Model
    ↓
PostgreSQL
```

Handler processes Telegram events: commands, buttons, and user messages.

Service contains application logic: user creation, section texts, the step-by-step request form, validation, and manager notification preparation.

Repository handles database access.

Model describes PostgreSQL tables through SQLAlchemy ORM.

## Project Structure

```text
app/
├── config/          # project settings
├── db/              # database connection
├── handlers/        # Telegram handlers
├── keyboards/       # Telegram keyboards
├── models/          # SQLAlchemy ORM models
├── repositories/    # data access layer
├── services/        # application logic
└── errors.py        # domain errors

migrations/          # Alembic migrations
main.py              # application entry point
docker-compose.yml   # local PostgreSQL
```

## Main User Flow

```text
/start
→ main menu
→ user selects a section
→ user clicks "Submit Request"
→ bot asks questions one by one
→ user fills required fields
→ optional fields can be skipped
→ request is saved to the database
→ manager receives a notification
→ user receives confirmation
```

## Environment Variables

Create `.env` from `.env.example`:

```env
BOT_TOKEN=your_telegram_bot_token
MANAGER_CHAT_ID=your_telegram_id

POSTGRES_DB=food_bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

`BOT_TOKEN` is issued by BotFather.

`MANAGER_CHAT_ID` is the Telegram ID of the user who receives new request notifications.

## Local Setup

Install dependencies:

```bash
poetry install
```

Start PostgreSQL:

```bash
docker compose up -d
```

Check the database connection:

```bash
poetry run python -c "from sqlalchemy import text; from app.db.database import engine; conn = engine.connect(); print(conn.execute(text('select 1')).scalar()); conn.close()"
```

Apply migrations:

```bash
poetry run alembic upgrade head
```

Run the bot:

```bash
poetry run python main.py
```

After startup, open the bot in Telegram and send `/start`.

## Checks

Check Python syntax:

```bash
poetry run python -m compileall app main.py
```

Check the current migration:

```bash
poetry run alembic current
```

View recent requests in the database:

```bash
poetry run python - <<'PY'
from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.application import Application

with SessionLocal() as session:
    applications = session.scalars(
        select(Application).order_by(Application.id.desc()).limit(5)
    ).all()

    for application in applications:
        print(
            f"id={application.id}, "
            f"name={application.name}, "
            f"phone={application.phone}, "
            f"status={application.notification_status}"
        )
PY
```

## MVP Scope

The project intentionally does not include:

- promotion filtering by client type;
- CRM or admin panel;
- Telegram Web App form;
- online payments;
- manager-side request processing inside the bot;
- multiple user roles;
- admin command for exporting requests.

These features are outside the current portfolio version. The MVP focuses on the main user path: information → request → manager notification.
