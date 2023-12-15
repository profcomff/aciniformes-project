from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aciniformes_backend.settings import get_settings


settings = get_settings()

engine = create_engine(str(settings.DB_DSN), execution_options={"isolation_level": "AUTOCOMMIT", "pool_pre_ping": True})
session_factory = sessionmaker(bind=engine)