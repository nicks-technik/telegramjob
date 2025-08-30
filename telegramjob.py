import os
import random
import re
from time import sleep
from telethon.sync import TelegramClient
from datetime import datetime
import telegramstuff  # Read the messages from the Telegram channel
from logger_config import logger
from playwrightstuff import PlaywrightBrowser
from message_parser import extract_jobs_from_messages
from config import Config

api_id: int = Config.API_ID
api_hash: str = Config.API_HASH
destination_chat_id: int = Config.DESTINATION_CHAT_ID
source_chat_id: int = Config.SOURCE_CHAT_ID
wait_min: int = Config.WAIT_MIN
wait_max: int = Config.WAIT_MAX
telegram_limit: int = Config.TELEGRAM_LIMIT


def random_sleep(min: int, max: int) -> None:
    """Pauses the execution of the program for a random amount of time between 60 and 180 seconds.
    The function generates a random integer between 60 and 180 (inclusive) and then
    logs this value. It then pauses the execution for the generated number of seconds.
    Returns:
        None
    """
    sleep_time = random.randint(min, max)
    logger.warning(f"Sleeping for {sleep_time} seconds...")
    sleep(sleep_time)


async def process_job(job, client, destination_chat_id):
    """
    Processes a single job: takes a screenshot, and sends it via Telegram.
    """
    logger.warning(f"Job: {job}")
    url = job["url"]
    task_number = job["task_number"]
    today = datetime.now().strftime("%y%m%d")
    new_filename = f"{today}_{task_number}.png"

    if os.path.exists(f"./png/{new_filename}"):
        logger.warning(
            f"Screenshot already exists for task: {task_number}. Filename: {new_filename} Skipping."
        )
        return

    browser = PlaywrightBrowser()
    try:
        await browser.launch()
        await browser.take_screenshot(url, new_filename)
    finally:
        await browser.close()

    if await telegramstuff.send_picture(
        client, destination_chat_id, new_filename, task_number
    ):
        logger.warning(f"DONE: {job}")
    else:
        logger.error(f"ERROR ERROR ERROR Failed to send picture for job: {job}")


async def main() -> None:
    dialogs = await client.get_dialogs()

    messages = await telegramstuff.scrape_message(
        client, source_chat_id, limit=telegram_limit
    )
    logger.debug(f"Message List: {messages}")

    jobs = extract_jobs_from_messages(messages)

    logger.info(f"Found jobs: {jobs}")

    if not jobs:
        logger.warning("No jobs found.")
        return

    # Process only the first job (most recent from scrape_message)
    job = jobs[0]
    await process_job(job, client, destination_chat_id)


if __name__ == "__main__":
    random_sleep(wait_min, wait_max)
    client = TelegramClient("telegram", Config.API_ID, Config.API_HASH)
    logger.info("After TelegramClient")

    with client:
        client.loop.run_until_complete(main())
