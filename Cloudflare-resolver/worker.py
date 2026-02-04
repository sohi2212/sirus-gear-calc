import asyncio
from app.queue import task_queue
from app.camoufox_manager import camoufox_manager

async def worker():
    await camoufox_manager.start()

    while True:
        task = await task_queue.get()

        try:
            status, content = await camoufox_manager.fetch(task["url"])
            task["future"].set_result((status, content))

        except Exception as e:
            task["future"].set_exception(e)

        finally:
            task_queue.task_done()
