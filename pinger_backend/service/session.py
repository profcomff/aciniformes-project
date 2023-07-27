from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from settings import get_settings


settings = get_settings()

engine = create_engine(str(settings.DB_DSN), execution_options={"isolation_level": "AUTOCOMMIT", "pool_pre_ping": True})
session = sessionmaker(bind=engine)


def dbsession() -> Session:
    global session
    localsession = session()

    return localsession
