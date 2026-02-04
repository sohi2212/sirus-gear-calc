import asyncio
from app.settings import settings

task_queue: asyncio.Queue = asyncio.Queue(
    maxsize=settings.QUEUE_SIZE
)
