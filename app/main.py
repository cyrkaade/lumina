
from fastapi import FastAPI
from app.api import calls, analytics

app = FastAPI()

app.include_router(calls.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")