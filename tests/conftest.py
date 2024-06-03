import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from aciniformes_backend.models.base import BaseModel
from aciniformes_backend.routes.base import app
from aciniformes_backend.settings import get_settings


@pytest.fixture(scope="session")
def engine():
    return create_engine(str(get_settings().DB_DSN), execution_options={"isolation_level": "AUTOCOMMIT"})


@pytest.fixture(scope="session")
def dbsession(engine):
    connection = engine.connect()
    session = Session(bind=connection, autoflush=False)
    yield session
    session.close()
    connection.close()


@pytest.fixture
def crud_client():
    client = TestClient(app)
    settings = get_settings()
    settings.BACKEND_URL = "http://testserver"
    return client
