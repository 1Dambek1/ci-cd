from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, Generator

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app import crud, models
from app.config import Settings, load_settings
from app.db import Base, create_engine_and_session
from app.schemas import TaskCreate, TaskRead, TaskUpdate


def get_session(request: Request) -> Generator[Session, None, None]:
    session_local = request.app.state.session_local
    session = session_local()
    try:
        yield session
    finally:
        session.close()


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or load_settings()
    engine, session_local = create_engine_and_session(app_settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield
        engine.dispose()

    app = FastAPI(
        title=app_settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )
    app.state.settings = app_settings
    app.state.engine = engine
    app.state.session_local = session_local

    @app.get("/")
    def root() -> dict[str, Any]:
        return {
            "service": app_settings.app_name,
            "environment": app_settings.app_env,
            "docs": "/docs",
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "service": app_settings.app_name,
            "environment": app_settings.app_env,
        }

    @app.get("/tasks", response_model=list[TaskRead])
    def get_tasks(session: Session = Depends(get_session)) -> list[models.Task]:
        return crud.list_tasks(session)

    @app.get("/tasks/{task_id}", response_model=TaskRead)
    def get_task(task_id: int, session: Session = Depends(get_session)) -> models.Task:
        task = crud.get_task(session, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    @app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
    def create_task(
        payload: TaskCreate,
        session: Session = Depends(get_session),
    ) -> models.Task:
        return crud.create_task(session, payload)

    @app.patch("/tasks/{task_id}", response_model=TaskRead)
    def update_task(
        task_id: int,
        payload: TaskUpdate,
        session: Session = Depends(get_session),
    ) -> models.Task:
        task = crud.get_task(session, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return crud.update_task(session, task, payload)

    @app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_task(task_id: int, session: Session = Depends(get_session)) -> Response:
        task = crud.get_task(session, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        crud.delete_task(session, task)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
