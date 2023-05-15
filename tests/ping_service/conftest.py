import pytest
from fastapi.testclient import TestClient

from aciniformes_backend.routes import app
from aciniformes_backend.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from aciniformes_backend.models.base import BaseModel
from pinger_backend.service import Config


@pytest.fixture(scope="session")
def fake_config():
    Config.fake = False
    conf = Config()
    yield conf


@pytest.fixture(scope="session")
def crud_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def dbsession() -> Session:
    settings = get_settings()
    engine = create_engine(settings.DB_DSN, execution_options={"isolation_level": "AUTOCOMMIT"})
    TestingSessionLocal = sessionmaker(bind=engine)
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
