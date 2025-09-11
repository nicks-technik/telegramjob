"""This script automates the process of extracting job information from Telegram messages,
taking screenshots of associated links, and sending them via Telegram.
"""

import argparse  # Added this import
import os
import random
from datetime import datetime
from time import sleep

from telethon.sync import TelegramClient

import telegramstuff  # type: ignore

# Read the messages from the Telegram channel
from config import Config
from logger_config import logger
from message_parser import extract_jobs_from_messages
from playwrightstuff import PlaywrightBrowser
from youtube_api import YouTubeAPI


# --- Argument Parsing ---
# Setup command-line argument parsing to allow for a configurable .env file path.
parser = argparse.ArgumentParser(description="Telegram Job Scraper")
parser.add_argument(
    "--env-file",
    type=str,
    default=".env",
    help="Path to the .env file to load (default: .env)",
)
args = parser.parse_args()

# --- Configuration Loading ---
# Resolve the .env file path to an absolute path to ensure it's found correctly.
env_file_path = os.path.abspath(args.env_file)

# Load the environment variables from the specified .env file and initialize the configuration.
Config.load_env_file(env_file_path)
Config.init_config()

# --- Configuration Variables ---
# Telegram API credentials
api_id: int = Config.API_ID
api_hash: str = Config.API_HASH

# Telegram chat IDs
destination_chat_id: int = Config.DESTINATION_CHAT_ID
source_chat_id: int = Config.SOURCE_CHAT_ID

# Script behavior settings
wait_min: int = Config.WAIT_MIN  # Minimum random sleep time in seconds
wait_max: int = Config.WAIT_MAX  # Maximum random sleep time in seconds
telegram_limit: int = Config.TELEGRAM_LIMIT  # Number of messages to fetch

# File paths
client_secrets_file: str = Config.CLIENT_SECRETS_FILE
storage_state_path: str = Config.STORAGE_STATE_PATH
youtube_engaged = Config.YOUTUBE_ENGAGED


def random_sleep(min_val: int, max_val: int) -> None:
    """Pauses execution for a random duration between min_val and max_val seconds."""
    sleep_time = random.randint(min_val, max_val)
    logger.info(f"Sleeping for {sleep_time} seconds...")
    sleep(sleep_time)


async def process_job(job, client, destination_chat_id):
    """
    Processes a single job by taking a screenshot of its URL and sending it to a Telegram chat.

    This function will skip processing if a screenshot for the job already exists.

    Args:
        job (dict): A dictionary containing job details, including 'url' and 'task_number'.
        client (TelegramClient): The active Telegram client instance.
        destination_chat_id (int): The ID of the Telegram chat to send the screenshot to.
    """
    logger.info(f"Processing job: {job}")
    url = job["url"]
    task_number = job["task_number"]
    today = datetime.now().strftime("%y%m%d")
    new_filename = f"{today}_{task_number}.png"

    # Avoid re-processing by checking if the screenshot already exists.
    if os.path.exists(f"./png/{new_filename}"):
        logger.warning(
            f"Screenshot already exists for task: {task_number}. Filename: {new_filename} Skipping."
        )
        return
    if youtube_engaged:
        if not client_secrets_file:
            raise ValueError(
                "YouTube client secrets file not found. Please set the path in your .env file."
            )
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        youtube_api = YouTubeAPI(client_secrets_file, scopes)

        # Example URL
        video_url = url
        video_id = youtube_api.get_video_id(video_url)

        if video_id:
            youtube_api.like_video(video_id)
            channel_id = youtube_api.get_channel_id_from_video(video_id)
            if channel_id:
                youtube_api.subscribe_to_channel(channel_id)

    logger.info(f"Attempting to take screenshot for URL: {url}")

    # Launch a browser, take a screenshot, and ensure the browser is closed.
    browser = PlaywrightBrowser()
    try:
        await browser.launch()
        await browser.take_screenshot(url, new_filename)
    finally:
        await browser.close()

    # Send the screenshot to the destination chat.
    if await telegramstuff.send_picture(
        client, destination_chat_id, new_filename, task_number
    ):
        logger.info(f"Successfully processed job: {job}")
    else:
        logger.error(f"Failed to send picture for job: {job}")


async def main() -> None:
    """
    Main asynchronous function to run the job scraping and processing workflow.

    This function fetches messages, extracts jobs, and processes the most recent one.
    """
    # Scrape recent messages from the source chat.
    messages = await telegramstuff.scrape_message(
        client, source_chat_id, limit=telegram_limit
    )
    logger.debug(f"Message List: {messages}")

    # Extract job information from the scraped messages.
    jobs = extract_jobs_from_messages(messages)

    logger.info(f"Found {len(jobs)} jobs.")
    logger.debug(f"Jobs: {jobs}")

    if not jobs:
        logger.warning("No jobs found in the latest messages.")
        return

    # The script is designed to process only the most recent job found.
    # `scrape_message` returns messages in descending order, so the first job in the list is the newest.
    job = jobs[0]
    await process_job(job, client, destination_chat_id)


if __name__ == "__main__":
    # Introduce a random delay before starting to mimic more human-like behavior.
    random_sleep(wait_min, wait_max)

    # Initialize and connect the Telegram client.
    logger.info("Initializing Telegram client...")
    client = TelegramClient("telegram", Config.API_ID, Config.API_HASH)

    with client:
        # Run the main asynchronous event loop.
        client.loop.run_until_complete(main())
