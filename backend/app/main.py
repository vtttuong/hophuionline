from fastapi import Request, FastAPI
from datetime import datetime

import asyncio
import json

app = FastAPI()

async def coroutine_echo_data(data):
    return data

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post('/results')
async def get_body(request: Request):
    data = await request.json()

    return coroutine_echo_data(data)