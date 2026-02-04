from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    QUEUE_SIZE: int = 100
    PAGE_TIMEOUT: int = 30_000
    BROWSER_RESTART_AFTER: int = 100  # запросов

settings = Settings()
