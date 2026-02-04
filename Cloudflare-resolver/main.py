import asyncio
from fastapi import FastAPI, HTTPException

from app.schemas import FetchRequest, FetchResponse
from app.queue import task_queue
from app.worker import worker

app = FastAPI(title="Camoufox API")

@app.on_event("startup")
async def startup():
    asyncio.create_task(worker())

@app.post("/fetch", response_model=FetchResponse)
async def fetch(req: FetchRequest):
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    try:
        await task_queue.put({
            "url": str(req.url),
            "future": future,
        })
    except asyncio.QueueFull:
        raise HTTPException(429, "Queue is full")

    try:
        status, content = await future
    except Exception as e:
        raise HTTPException(500, str(e))

    return FetchResponse(
        url=str(req.url),
        status=status,
        content=content,
    )
