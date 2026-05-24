from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def list_tasks(session: Session) -> list[Task]:
    statement = select(Task).order_by(Task.id)
    return list(session.scalars(statement).all())


def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def create_task(session: Session, payload: TaskCreate) -> Task:
    task = Task(
        title=payload.title,
        description=payload.description,
        status=payload.status,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def update_task(session: Session, task: Task, payload: TaskUpdate) -> Task:
    data = payload.model_dump(exclude_unset=True)
    for field_name, value in data.items():
        setattr(task, field_name, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task: Task) -> None:
    session.delete(task)
    session.commit()
