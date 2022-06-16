from fastapi import Request, FastAPI
from datetime import datetime

import asyncio
import json
import psycopg2, os

async def get_db_conn():
    return psycopg2.connect(
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"), port= os.getenv("DB_PORT"), sslmode=os.getenv("DB_SSL_MODE")
    )

app = FastAPI()

async def coroutine_echo_data(data):
    return data

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/db_version")
async def db_version():

    conn = await get_db_conn()
    cursor = conn.cursor()
    cursor.execute("select version()")

    data = cursor.fetchone()

    # please close conn manually
    conn.close()

    return f"Connection established to: {data}"

@app.post('/results')
async def get_body(request: Request):
    data = await request.json()

    return coroutine_echo_data(data)