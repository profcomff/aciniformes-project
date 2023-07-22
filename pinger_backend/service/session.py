from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .settings import get_settings as db_settings


def dbsession() -> Session:
    settings = db_settings()
    engine = create_engine(str(settings.DB_DSN), execution_options={"isolation_level": "AUTOCOMMIT"})
    session = sessionmaker(bind=engine)
    Base = declarative_base()
    localsession = session()
    Base.metadata.create_all(engine)

    return localsession
