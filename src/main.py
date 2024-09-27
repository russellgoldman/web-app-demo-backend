from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import health, mssql, json
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS").split(";"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(health.router, prefix="/health")
app.include_router(mssql.router, prefix="/mssql")
app.include_router(json.router, prefix="/json")
