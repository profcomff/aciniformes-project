import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from aciniformes_backend.settings import get_settings
from aciniformes_backend.models.base import BaseModel
from aciniformes_backend.routes.base import app
from aciniformes_backend.serivce import Config
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        get_settings().DB_DSN, execution_options={"isolation_level": "AUTOCOMMIT"}
    )


@pytest.fixture(scope="session")
def tables(engine):
    BaseModel.metadata.create_all(engine)
    yield
    # truncate all tables
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)


@pytest.fixture(scope="session")
def dbsession(engine, tables):
    connection = engine.connect()
    session = Session(bind=connection, autoflush=False)
    yield session
    session.close()
    connection.close()


@pytest.fixture(scope="session")
def fake_config():
    Config.fake = True
    conf = Config()
    yield conf


@pytest.fixture
def client(fake_config):
    client = TestClient(app)
    return client
