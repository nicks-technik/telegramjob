"""This script automates the process of extracting job information from Telegram messages,
taking screenshots of associated YouTube links, and sending them via Telegram.
"""

import argparse  # Added this import
import os
import random
from datetime import datetime
from time import sleep

from telethon.sync import TelegramClient

import telegramstuff  # Read the messages from the Telegram channel
from config import Config
from logger_config import logger
from message_parser import extract_jobs_from_messages
from playwrightstuff import PlaywrightBrowser

# Added argparse setup
parser = argparse.ArgumentParser(description="Telegram Job Scraper")
parser.add_argument(
    "--env-file",
    type=str,
    default=".env",
    help="Path to the .env file to load (default: .env)",
)
args = parser.parse_args()

# Resolve the .env file path to an absolute path
env_file_path = os.path.abspath(args.env_file)

# Pass the absolute env_file path to Config
Config.load_env_file(env_file_path)
Config.init_config()  # Call init_config to load values after .env is loaded

api_id: int = Config.API_ID
api_hash: str = Config.API_HASH
destination_chat_id: int = Config.DESTINATION_CHAT_ID
source_chat_id: int = Config.SOURCE_CHAT_ID
wait_min: int = Config.WAIT_MIN
wait_max: int = Config.WAIT_MAX
telegram_limit: int = Config.TELEGRAM_LIMIT
auth_file: str = Config.AUTH_FILE


def random_sleep(min_val: int, max_val: int) -> None:
    """Pauses the execution of the program for a random amount of time.
    The function generates a random integer between min_val and max_val (inclusive) and then
    logs this value. It then pauses the execution for the generated number of seconds.
    Args:
        min_val (int): The minimum number of seconds to sleep.
        max_val (int): The maximum number of seconds to sleep.
    """
    sleep_time = random.randint(min_val, max_val)
    logger.info(f"Sleeping for {sleep_time} seconds...")
    sleep(sleep_time)


async def process_job(job, client, destination_chat_id):
    """
    Processes a single job: takes a screenshot, and sends it via Telegram.
    """
    logger.info(f"Processing job: {job}")
    url = job["url"]
    task_number = job["task_number"]
    today = datetime.now().strftime("%y%m%d")
    new_filename = f"{today}_{task_number}.png"

    if os.path.exists(f"./png/{new_filename}"):
        logger.warning(
            f"Screenshot already exists for task: {task_number}. Filename: {new_filename} Skipping."
        )
        return

    # Check for YouTube action
    # video_id = extract_video_id(url)

    browser = PlaywrightBrowser()
    try:
        await browser.launch()
        await browser.take_screenshot(url, new_filename)
    finally:
        await browser.close()

    if await telegramstuff.send_picture(
        client, destination_chat_id, new_filename, task_number
    ):
        logger.info(f"Successfully processed job: {job}")
    else:
        logger.error(f"Failed to send picture for job: {job}")


async def main() -> None:
    """
    The main function of the application.
    """
    messages = await telegramstuff.scrape_message(
        client, source_chat_id, limit=telegram_limit
    )
    logger.debug(f"Message List: {messages}")

    jobs = extract_jobs_from_messages(messages)

    logger.info(f"Found {len(jobs)} jobs.")
    logger.debug(f"Jobs: {jobs}")

    if not jobs:
        logger.warning("No jobs found.")
        return

    # Process only the first job (most recent from scrape_message)
    job = jobs[0]
    await process_job(job, client, destination_chat_id)


if __name__ == "__main__":
    random_sleep(wait_min, wait_max)
    client = TelegramClient("telegram", Config.API_ID, Config.API_HASH)
    logger.info("Telegram client created.")

    with client:
        client.loop.run_until_complete(main())
