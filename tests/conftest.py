import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from aciniformes_backend.routes.base import app
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models.base import BaseModel


@pytest.fixture(scope='session')
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def engine():
    return create_engine(get_settings().DB_DSN)


@pytest.fixture(scope="session")
def tables(engine):
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    connection = engine.connect()
    session = Session(bind=connection, autocommit=True, autoflush=False)
    yield session
    session.close()
    connection.close()
