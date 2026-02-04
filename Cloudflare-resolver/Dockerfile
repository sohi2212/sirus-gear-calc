FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libasound2 \
    libgtk-3-0 libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Прогрев Camoufox
RUN python - <<EOF
from camoufox.async_api import AsyncCamoufox
import asyncio

async def main():
    c = AsyncCamoufox(headless=True)
    await c.start()
    await c.stop()

asyncio.run(main())
EOF

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
