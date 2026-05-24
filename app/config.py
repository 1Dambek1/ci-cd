from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    app_name: str
    app_env: str
    app_secret_key: str
    database_url: str


def load_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Project4 API"),
        app_env=os.getenv("APP_ENV", "development"),
        app_secret_key=os.getenv("APP_SECRET_KEY", "dev-secret-change-me"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./data/app.db"),
    )
