import asyncio
from camoufox.async_api import AsyncCamoufox
from app.settings import settings

class CamoufoxManager:
    def __init__(self):
        self._camoufox: AsyncCamoufox | None = None
        self._context = None
        self._lock = asyncio.Lock()
        self._requests_count = 0

    async def start(self):
        async with self._lock:
            if self._camoufox:
                return

            self._camoufox = AsyncCamoufox(
                headless=True,
                locale="en-US",
                timezone="UTC",
                window=(1280, 800),
            )

            await self._camoufox.start()
            self._context = await self._camoufox.new_context()
            self._requests_count = 0

    async def stop(self):
        async with self._lock:
            if self._camoufox:
                try:
                    await self._camoufox.stop()
                finally:
                    self._camoufox = None
                    self._context = None

    async def restart(self):
        await self.stop()
        await self.start()

    async def fetch(self, url: str):
        if not self._camoufox:
            await self.start()

        self._requests_count += 1

        if self._requests_count >= settings.BROWSER_RESTART_AFTER:
            await self.restart()

        page = await self._context.new_page()
        try:
            response = await page.goto(
                url,
                timeout=settings.PAGE_TIMEOUT,
                wait_until="networkidle",
            )
            content = await page.content()
            return response.status, content

        except Exception:
            # self-healing при любой ошибке браузера
            await self.restart()
            raise

        finally:
            await page.close()

camoufox_manager = CamoufoxManager()
