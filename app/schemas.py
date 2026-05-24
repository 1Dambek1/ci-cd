from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

TaskStatus = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus = "todo"


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)
    status: TaskStatus | None = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
