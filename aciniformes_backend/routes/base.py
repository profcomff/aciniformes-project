from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from aciniformes_backend.settings import get_settings
from aciniformes_backend import __version__

from .alert import router as alert_router
from .fetcher import router as fetcher_router
from .mectric import router as metric_router
from .reciever import router as receiver_router


settings = get_settings()
app = FastAPI(
    title='Сервис проверки доступности серверов',
    version=__version__,
    # Настраиваем интернет документацию
    docs_url=None if __version__ != 'dev' else '/docs',
    redoc_url=None,
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=str(get_settings().DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(alert_router, prefix="/alert", tags=["Alert"])
app.include_router(receiver_router, prefix="/receiver", tags=["Receiver"])
app.include_router(fetcher_router, prefix="/fetcher", tags=["Fetcher"])
app.include_router(metric_router, prefix="/metric", tags=["Metric"])
