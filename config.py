"""Configuration settings for the Telegram Job project."""

import os

from dotenv import load_dotenv
from logger_config import logger  # Import logger


class Config:
    """Stores all configuration settings for the application."""

    @staticmethod
    def load_env_file(env_path: str = ".env"):
        """Loads environment variables from the specified .env file."""
        logger.info(f"Attempting to load .env file from: {env_path}")
        loaded = load_dotenv(dotenv_path=env_path, override=True)
        logger.info(f".env file loaded successfully: {loaded}")
        if not loaded:
            logger.warning(
                f"Failed to load .env file from: {env_path}. Check path and permissions."
            )

    @staticmethod
    def init_config():
        """Initializes or re-initializes Config attributes from environment variables."""
        Config.API_ID = int(os.getenv(key="ENV_API_ID", default="0"))
        Config.API_HASH = os.getenv(key="ENV_API_HASH", default="")
        Config.DESTINATION_CHAT_ID = int(
            os.getenv("ENV_DESTINATION_CHAT_ID", default="0")
        )
        Config.SOURCE_CHAT_ID = int(os.getenv("ENV_SOURCE_CHAT_ID", default="0"))
        Config.WAIT_MIN = int(os.getenv("ENV_WAIT_MIN", default="60"))
        Config.WAIT_MAX = int(os.getenv("ENV_WAIT_MAX", default="300"))
        print(f"WAIT_MAX: {Config.WAIT_MAX}")
        Config.TELEGRAM_LIMIT = int(os.getenv("ENV_TELEGRAM_LIMIT", default="100"))
        Config.HEADLESS = (
            os.getenv(key="ENV_HEADLESS", default="False").lower() == "true"
        )
        # Config.AUTH_FILE = os.getenv(key="ENV_AUTH_FILE", default="credentials").lower()
        Config.CLIENT_SECRETS_FILE = os.getenv(
            key="ENV_CLIENT_SECRETS_FILE", default="client_secret.json"
        )
        print(f"Client Secrets File: {Config.CLIENT_SECRETS_FILE}")
        Config.STORAGE_STATE_PATH = os.getenv(
            key="ENV_STORAGE_STATE_PATH", default="youtube_state.json"
        )

        Config.SPECIFIC_TEXTS = os.getenv(key="ENV_SPECIFIC_TEXTS", default="").split(
            ","
        )
        logger.info(
            f"Config initialized. API_ID: {Config.API_ID}, API_HASH: {Config.API_HASH[:5]}..."
        )  # Log first 5 chars of hash

    # Initialize with default values, will be updated by init_config()
    API_ID: int = 0
    API_HASH: str = ""
    DESTINATION_CHAT_ID: int = 0
    SOURCE_CHAT_ID: int = 0
    WAIT_MIN: int = 0
    WAIT_MAX: int = 0
    TELEGRAM_LIMIT: int = 0
    HEADLESS: bool = False
    # AUTH_FILE: str = ""  # New: path to Playwright auth file
    CLIENT_SECRETS_FILE = ""
    STORAGE_STATE_PATH = ""
    SPECIFIC_TEXTS: list[str] = []
