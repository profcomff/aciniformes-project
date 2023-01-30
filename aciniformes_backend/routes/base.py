from fastapi import FastAPI
from .alert.alert import router as alert_router
from .alert.reciever import router as receiver_router
from .fetcher import router as fetcher_router
from .mectric import router as metric_router
from fastapi_sqlalchemy import DBSessionMiddleware
from aciniformes_backend.settings import get_settings


app = FastAPI()
app.include_router(alert_router, prefix="/alert")
app.include_router(receiver_router, prefix="/receiver")
app.include_router(fetcher_router, prefix="/fetcher")
app.include_router(metric_router, prefix="/metric")

app.add_middleware(
    DBSessionMiddleware,
    db_url=get_settings().DB_DSN,
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)
