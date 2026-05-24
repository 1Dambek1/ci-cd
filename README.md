# Project4 Backend

`project4` is a ready-to-use `FastAPI` backend template with:

- a simple tasks API
- automated tests with `pytest`
- linting with `ruff`
- containerization with `Docker`
- GitHub Actions for `CI` and `CD`

## Stack

- `Python 3.12`
- `FastAPI`
- `SQLAlchemy`
- `SQLite` by default
- `uv`
- `pytest`
- `GitHub Actions`

## Endpoints

- `GET /`
- `GET /health`
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

## Local run

Copy the example env file:

```bash
cp .env.example .env
```

Install dependencies:

```bash
uv sync
```

If you already have another virtual environment activated, open a fresh terminal or run without the active environment. `uv` should use the local `project4/.venv`.

Run the backend:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

Swagger:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Tests

Run tests:

```bash
uv run pytest
```

Run lint:

```bash
uv run ruff check .
```

## Docker

Build and run:

```bash
docker compose up --build
```

## GitHub CI

Workflow file:

- `.github/workflows/ci.yml`

What it does:

- installs dependencies with `uv`
- runs `ruff`
- runs `pytest` with coverage

## GitHub CD

Workflow file:

- `.github/workflows/cd.yml`

What it does:

1. builds a Docker image
2. pushes it to `GHCR`
3. optionally deploys it to a VPS over `SSH`

## Secrets for CD

Create these GitHub secrets before enabling deployment:

- `VPS_HOST`
- `VPS_USER`
- `VPS_SSH_KEY`
- `GHCR_USERNAME`
- `GHCR_TOKEN`
- `APP_SECRET_KEY`
- `DATABASE_URL`

Optional:

- if you skip these secrets, the deploy step will be skipped, but image publishing to `GHCR` will still work

## Deploy notes

The deploy workflow runs a single Docker container on the server:

- container name: `project4-backend`
- host port: `8000`
- container port: `8000`

If you want `HTTPS` and a domain later, place `Nginx` or `Caddy` in front of it on the VPS.
