from fastapi import HTTPException
import pymssql
from dotenv import load_dotenv, find_dotenv
import os

# Automatically find and load the .env file starting from the current directory and moving up
load_dotenv(find_dotenv())

def get_mssql_conn():
    try:
        conn = pymssql.connect(
            server=os.getenv("MSSQL_SERVER"),
            user=os.getenv("MSSQL_USER"),
            password=os.getenv("MSSQL_PASSWORD"),
            database=os.getenv("MSSQL_DATABASE"),
            port=os.getenv("MSSQL_PORT"),
        )
        return conn
    except pymssql.Error as e:
        raise HTTPException(status_code=500, detail=str(e))