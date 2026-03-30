# BlogApp API

A simple open blog REST API — anyone can create users and write posts. Built as a portfolio project to demonstrate secure credential handling, industry-standard project structure, and containerised deployment with Docker.

Live API: *coming soon (Railway)*

---

## What's inside

- **FastAPI** — modern async Python web framework with automatic Swagger docs
- **SQLAlchemy 2** — ORM with proper relationship handling and cascading deletes
- **MySQL 8** — relational database
- **Pydantic v2** — request validation with field-level rules (not just types)
- **pydantic-settings** — environment-based config that hard-fails on missing secrets
- **Docker + Compose** — containerised app and database, wired together with healthchecks
- **Uvicorn** — ASGI server

---

## Project structure

```
blogApp/
├── app/
│   ├── main.py        # App init, CORS middleware, router registration
│   ├── config.py      # All settings loaded from .env via pydantic-settings
│   ├── database.py    # SQLAlchemy engine, session, Base
│   ├── models.py      # Database table definitions
│   ├── schemas.py     # Pydantic request/response schemas with validators
│   └── routers/
│       ├── users.py   # /users endpoints
│       └── posts.py   # /posts endpoints
├── .env.example       # Environment variable template — copy to .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Running locally with Docker

This is the recommended way — no local Python or MySQL setup needed.

**1. Clone the repo**
```bash
git clone https://github.com/rohan-sm/blogApp
cd blogApp
```

**2. Set up your environment**
```bash
cp .env.example .env
# open .env and set your own passwords
```

**3. Start everything**
```bash
docker compose up --build
```

Docker will pull MySQL, build the app image, and start both containers. The API waits for MySQL to pass its healthcheck before starting — no race conditions.

**4. Open the docs**
```
http://localhost:8000/docs
```

That's it. No virtual environments, no local MySQL, no manual table creation.

---

## Running locally without Docker

If you'd rather run it the traditional way:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Set up `.env` with `DB_HOST=localhost` and make sure your local MySQL is running with a database named `blogapplication`.

```bash
uvicorn app.main:app --reload
```

---

## Environment variables

Copy `.env.example` to `.env` and fill in your values. Never commit `.env` — it's gitignored.

| Variable | Description | Required |
|----------|-------------|----------|
| `DB_USER` | MySQL username | yes |
| `DB_PASSWORD` | MySQL password | yes |
| `DB_HOST` | MySQL host (`db` for Docker, `localhost` for local) | yes |
| `DB_PORT` | MySQL port | yes (default 3306) |
| `DB_NAME` | Database name | yes |
| `DB_ROOT_PASSWORD` | MySQL root password (used by Docker Compose) | yes |
| `ALLOWED_ORIGINS` | CORS origins, comma-separated | yes (use `*` for dev) |

The app uses `pydantic-settings` to load these — if any required variable is missing, the app refuses to start with a clear error rather than silently failing.

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/users/` | Create a user |
| `GET` | `/users/{id}` | Get a user by ID |
| `DELETE` | `/users/{id}` | Delete a user and all their posts |
| `POST` | `/posts/` | Create a post |
| `GET` | `/posts/` | List all posts (paginated) |
| `GET` | `/posts/{id}` | Get a post by ID |
| `DELETE` | `/posts/{id}` | Delete a post |
| `GET` | `/health` | Health check |

Full interactive docs available at `/docs` (Swagger UI) and `/redoc` (ReDoc).

---

## Validation rules

Requests are validated by Pydantic before touching the database.

**Users**
- `username` — 3 to 50 characters, alphanumeric only

**Posts**
- `title` — 3 to 200 characters
- `content` — 10 to 10,000 characters

Invalid requests get a descriptive 422 response — no crashes, no silent failures.

---

## Security decisions

- **No hardcoded credentials** — all secrets live in `.env`, loaded and validated at startup
- **`.env` is gitignored** — only `.env.example` (with fake values) is committed
- **Non-root container user** — the Docker image runs as an unprivileged user
- **Multi-stage Docker build** — final image contains no build tools or pip, smaller attack surface
- **CORS configured via env** — origins are not hardcoded, configurable per environment
- **Cascading deletes** — deleting a user cleans up their posts at the database level

---

## What's next

- [ ] Deploy to Railway (live URL)
- [ ] Alembic migrations instead of `create_all()`
- [ ] Pagination on `GET /posts/` with proper cursor support
- [ ] Rate limiting