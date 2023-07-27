from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from settings import get_settings

from .alert.alert import router as alert_router
from .alert.reciever import router as receiver_router
from .fetcher import router as fetcher_router
from .mectric import router as metric_router


app = FastAPI()
app.include_router(alert_router, prefix="/alert", tags=["Alert"])
app.include_router(receiver_router, prefix="/receiver", tags=["Receiver"])
app.include_router(fetcher_router, prefix="/fetcher", tags=["Fetcher"])
app.include_router(metric_router, prefix="/metric", tags=["Metric"])

app.add_middleware(
    DBSessionMiddleware,
    db_url=str(get_settings().DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)
