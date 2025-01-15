import os
import logging
from time import sleep
import re
from dotenv import load_dotenv
import telegrampart

# import playwrightpart
from telethon.sync import TelegramClient
import ytsubscribe

# import asyncio

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()
api_id: int = int(os.getenv(key="ENV_API_ID"))
api_hash: str = os.getenv(key="ENV_API_HASH")
destination_chat_id: int = int(os.getenv("ENV_DESTINATION_CHAT_ID"))
source_chat_id: int = int(os.getenv("ENV_SOURCE_CHAT_ID"))
import re
import random


def random_sleep() -> None:
    """
    Pauses the execution of the program for a random amount of time between 60 and 180 seconds.

    The function generates a random integer between 60 and 180 (inclusive) and then
    logs this value. It then pauses the execution for the generated number of seconds.

    Returns:
        None
    """
    sleep_time = random.randint(60, 180)
    logging.info(f"Sleeping for {sleep_time} seconds...")
    sleep(sleep_time)


def extract_video_id(url):
    """Extracts the YouTube video ID from a URL.

    Args:
        url (str): The YouTube URL.

    Returns:
        str: The extracted video ID, or None if not found.
    """
    if "youtu.be/" in url:
        try:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return video_id
        except IndexError:
            return None
    elif "youtube.com/watch?v=" in url:
        try:
            video_id = url.split("youtube.com/watch?v=")[1].split("&")[0].split("?")[0]
            return video_id
        except IndexError:
            return None
    else:
        return None


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
    logging.info("In Extracting info from messages...")
    extracted_data = []
    for message in messages:

        logging.debug(f"\n\n\n\n\nActual Message: {message}")

        searchstring = "veröffentlicht"
        if searchstring in message:
            logging.debug(f"The text {searchstring} is in the  {message}")
        else:
            logging.debug(f"The text {searchstring} is not in the {message}")
            continue

        searchstring = "https://youtu.be/"
        if searchstring in message:
            logging.debug(f"The text {searchstring} is in the  {message}")
        else:
            logging.debug(f"The text {searchstring} is not in the {message}")
            continue

        task_match = re.search(r"(Mission Nr\.|Aufgaben Nr\.)\s*(\d+)", message)
        logging.debug(f"Task Match: {task_match}")
        link_match = re.search(r"(https?://[^\s]+)", message)
        logging.debug(f"Link Match: {link_match}")
        if task_match and link_match:
            task_number = task_match.group(2)
            video_url = link_match.group(1)
            video_id = extract_video_id(video_url)
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

    messages = await telegrampart.scrape_message(client, source_chat_id, limit=200)

    logging.debug(f"Message List: {messages}")
    sleep(10)
    logging.info("Before Extracting info from messages...")
    jobs = extract_info_from_messages(messages)
    logging.debug(f"jobs: {jobs}")
    creds = ytsubscribe.check_login()
    for job in jobs:
        logging.debug(f"Job: {job}")
        video_url = job["video_url"]
        video_id = job["video_id"]

        if os.path.exists(f"./png/{video_id}.png"):
            logging.info(
                f"Screenshot already exists for video ID: {video_id}. Skipping."
            )
            continue

        if ytsubscribe.like_video(creds, video_id):
            logging.info(f"Successfully liked video: {video_id}")
            # channel_id = ytsubscribe.get_channel_id_from_video_id(creds, video_id)
            # if ytsubscribe.subscribe_to_channel(creds, channel_id):
            #     logging.info(f"Successfully liked and subscribed to video: {video_id}")

            os.system(f"python3 playwrightpart.py {video_url} {video_id}")

            await telegrampart.send_picture(
                client, destination_chat_id, job["video_id"], job["task_number"]
            )
            break  # for loop


if __name__ == "__main__":

    random_sleep()
    # asyncio.run(main())
    client = TelegramClient("telegram", api_id, api_hash)

    with client:
        client.loop.run_until_complete(main())
