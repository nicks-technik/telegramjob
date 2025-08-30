"""Configuration settings for the Telegram Job project."""

import os

from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    """Stores all configuration settings for the application."""

    API_ID: int = int(os.getenv(key="ENV_API_ID", default="0"))
    API_HASH: str = os.getenv(key="ENV_API_HASH", default="")
    DESTINATION_CHAT_ID: int = int(os.getenv("ENV_DESTINATION_CHAT_ID", default="0"))
    SOURCE_CHAT_ID: int = int(os.getenv("ENV_SOURCE_CHAT_ID", default="0"))
    WAIT_MIN: int = int(os.getenv("ENV_WAIT_MIN", default="60"))
    WAIT_MAX: int = int(os.getenv("ENV_WAIT_MAX", default="300"))
    TELEGRAM_LIMIT: int = int(os.getenv("ENV_TELEGRAM_LIMIT", default="100"))
    HEADLESS: bool = os.getenv(key="ENV_HEADLESS", default="False").lower() == "true"
    YOUTUBE_EMAIL: str = os.getenv(key="ENV_YOUTUBE_EMAIL", default="")
    YOUTUBE_PASSWORD: str = os.getenv(key="ENV_YOUTUBE_PASSWORD", default="")
    SPECIFIC_TEXTS: list[str] = os.getenv(key="ENV_SPECIFIC_TEXTS", default="").split(
        ","
    )
