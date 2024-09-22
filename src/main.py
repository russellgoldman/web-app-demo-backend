from fastapi import FastAPI
from src.api.endpoints import health, mssql

app = FastAPI()

app.include_router(health.router, prefix="/health")
app.include_router(mssql.router, prefix="/mssql")
