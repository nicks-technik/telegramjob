import sys
import os
import re
import random
from time import sleep
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from logger_config import logger
import telegramstuff
import youtubestuff

# import playwrightpart
load_dotenv(override=True)

api_id: int = int(os.getenv(key="ENV_API_ID", default="0"))
api_hash: str = os.getenv(key="ENV_API_HASH", default="")
destination_chat_id: int = int(os.getenv("ENV_DESTINATION_CHAT_ID"))  # type: ignore
source_chat_id: int = int(os.getenv("ENV_SOURCE_CHAT_ID"))  # type: ignore
wait_min: int = int(os.getenv("ENV_WAIT_MIN", default="60"))  # type: ignore
wait_max: int = int(os.getenv("ENV_WAIT_MAX", default="300"))  # type: ignore


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


def extract_info_from_messages(messages):
    """
    Extracts task numbers and YouTube links from a list of messages.

    Args:
        messages (list): A list of strings (messages).

    Returns:
        list: A list of dictionaries, where each dictionary contains
        the task number and youtube link,
        or an empty list if no data could be extracted.
    """
    logger.debug("In Extracting info from messages...")
    extracted_data = []
    for message in messages:

        logger.debug(f"\n\n\n\n\nActual Message: {message}")

        searchstring = "veröffentlicht"
        if searchstring in message:
            logger.debug(f"The text {searchstring} is in the  {message}")
        else:
            logger.debug(f"The text {searchstring} is not in the {message}")
            continue

        searchstring = "https://youtu.be/"
        if searchstring in message:
            logger.debug(f"The text {searchstring} is in the  {message}")
        else:
            logger.debug(f"The text {searchstring} is not in the {message}")
            continue

        task_match = re.search(r"(Mission Nr\.|Aufgaben Nr\.)\s*(\d+)", message)
        logger.debug(f"Task Match: {task_match}")
        link_match = re.search(r"(https?://[^\s]+)", message)
        logger.debug(f"Link Match: {link_match}")
        if task_match and link_match:
            task_number = task_match.group(2)
            video_url = link_match.group(1)
            video_id = youtubestuff.extract_video_id(video_url)
            # video_id = "test"

            extracted_data.append(
                {
                    "task_number": task_number,
                    "video_url": video_url,
                    "video_id": video_id,
                }
            )

    return extracted_data


async def main() -> None:

    dialogs = await client.get_dialogs()

    messages = await telegramstuff.scrape_message(client, source_chat_id, limit=200)
    logger.debug(f"Message List: {messages}")

    jobs = extract_info_from_messages(messages)
    logger.debug(f"Found jobs: {jobs}")

    creds = youtubestuff.check_login()

    for job in jobs:

        logger.debug(f"Job: {job}")
        video_url = job["video_url"]
        video_id = job["video_id"]
        task_text = job["task_number"]

        if os.path.exists(f"./png/{video_id}.png"):
            logger.warning(
                f"Screenshot already exists for video ID: {video_id}. Task: {task_text} Skipping."
            )
            break

        if youtubestuff.like_video(creds, video_id):
            logger.warning(f"Successfully liked video: {video_id}")
        else:
            channel_id = youtubestuff.get_channel_id_from_video_id(creds, video_id)
            if youtubestuff.subscribe_to_channel(creds, channel_id):
                logger.info(f"Successfully subscribed to video: {video_id}")
            else:
                logger.error(f"Failed to like and subscribe to video: {video_id}")
                sys.exit(1)

        os.system(f"python3 playwrightpart.py {video_url} {video_id}")

        await telegramstuff.send_picture(client, destination_chat_id, job)
        break


if __name__ == "__main__":
    # logger = setup_logger(console_level=logging.INFO)

    logger.warning("1030 1100 1300 1330 1530 1600 1800 1830 dealer task")
    random_sleep(wait_min, wait_max)
    # asyncio.run(main())
    client = TelegramClient("telegram", api_id, api_hash)

    with client:
        client.loop.run_until_complete(main())
