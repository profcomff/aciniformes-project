from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from aciniformes_backend.models.base import BaseModel
from aciniformes_backend.settings import get_settings as db_settings


def dbsession() -> Session:
    settings = db_settings()
    engine = create_engine(settings.DB_DSN, execution_options={"isolation_level": "AUTOCOMMIT"})
    session = sessionmaker(bind=engine)
    localsession = session()
    BaseModel.metadata.create_all(bind=engine)

    return localsession
