from fastapi import FastAPI
from .alert.alert import router as alert_router
from .alert.reciever import router as reciever_router
from .fetcher import router as fetcher_router
from .mectric import router as metric_router

app = FastAPI()
app.include_router(alert_router, prefix='/alert')
app.include_router(reciever_router, prefix='/reciever')
app.include_router(fetcher_router, prefix='/fetcher')
app.include_router(metric_router, prefix='/metric')
