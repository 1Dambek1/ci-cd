from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


@pytest.fixture()
def client():
    database_url = "sqlite:///./data/test.db"
    settings = Settings(
        app_name="Project4 Test API",
        app_env="test",
        app_secret_key="test-secret",
        database_url=database_url,
    )
    app = create_app(settings)
    with TestClient(app) as test_client:
        yield test_client
