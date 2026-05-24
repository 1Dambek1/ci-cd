from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


def _ensure_sqlite_directory(database_url: str) -> None:
    if not database_url.startswith("sqlite:///"):
        return

    raw_path = database_url.removeprefix("sqlite:///")
    if raw_path == ":memory:":
        return

    db_path = Path(raw_path)
    if db_path.parent != Path(""):
        db_path.parent.mkdir(parents=True, exist_ok=True)


def create_engine_and_session(database_url: str) -> tuple[object, sessionmaker[Session]]:
    _ensure_sqlite_directory(database_url)

    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    engine = create_engine(
        database_url,
        future=True,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
    session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=Session,
    )
    return engine, session_local
