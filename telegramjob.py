import os
import logging
import re
from dotenv import load_dotenv
import telegrampart
import playwrightpart
import ytsubscribe
from telethon.sync import TelegramClient
import asyncio

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

load_dotenv()
api_id: int = int(os.getenv(key="ENV_API_ID"))
api_hash: str = os.getenv(key="ENV_API_HASH")
destination_chat_id: int = int(os.getenv("ENV_DESTINATION_CHAT_ID"))
source_chat_id: int = int(os.getenv("ENV_SOURCE_CHAT_ID"))
import re


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
    extracted_data = []
    for message in messages:
        logging.info(f"Message: {message}")
        task_match = re.search(r"(Mission Nr\.|Aufgaben Nr\.)\s*(\d+)", message)
        logging.info(f"Task Match: {task_match}")
        link_match = re.search(r"(https?://[^\s]+)", message)
        logging.info(f"Link Match: {link_match}")
        if task_match and link_match:
            task_number = task_match.group(2)
            youtube_url = link_match.group(1)
            video_id = youtube_url.split("?v=")[1]

            extracted_data.append(
                {
                    "task_number": task_number,
                    "youtube_url": youtube_url,
                    "video_id": video_id,
                }
            )

    return extracted_data


async def main() -> None:
    # video_url = "https://www.youtube.com/watch?v=LNVXJUyaAhM"
    # video_id = video_url.split("?v=")[1]
    # task_text = "This is a test task"
    # logging.info(f"Video ID: {video_id}")

    dialogs = await client.get_dialogs()

    # messages = await telegrampart.scrape_message(client, source_chat_id, limit=120)
    messages = [
        "Some random text Mission Nr. 123 https://www.youtube.com/watch?v=dQw4w9WgXcQ another sentence",
        "Some other text Aufgabennr. 456 https://www.youtube.com/watch?v=DnvLbaRk",
        "A message without keywords",
        "Mission Nr. 789 no url here",
        "Aufgaben Nr. 124 https://www.youtube.com/watch?v=DnvLbaaWQRk some more text",
        "Another test message which has no number before the mission nr: Mission Nr. https://www.youtube.com/watch?v=zyxwvu0987",
    ]

    logging.info(f"Message List: {messages}")

    jobs = extract_info_from_messages(messages)
    logging.info(f"jobs: {jobs}")
    creds = ytsubscribe.check_login()
    for job in jobs:
        logging.info(f"Job: {job}")
        video_id = job["video_id"]

        if os.path.exists(f"./png/{video_id}.png"):
            logging.info(
                f"Screenshot already exists for video ID: {video_id}. Skipping."
            )
            continue

        if ytsubscribe.like_video(creds, video_id):
            channel_id = ytsubscribe.get_channel_id_from_video_id(creds, video_id)
            if ytsubscribe.subscribe_to_channel(creds, channel_id):
                logging.info(f"Successfully liked and subscribed to video: {video_id}")

                os.system(f"python3 playwrightpart.py {video_id}")

                await telegrampart.send_picture(
                    client, destination_chat_id, job["video_id"], job["task_number"]
                )

    #     if video_id in message:
    #         logging.info(f"Found video ID in message: {message}")
    #         await telegrampart.send_picture(
    #             client, destination_chat_id, video_id, task_text
    #         )
    #         break
    # else:
    #     logging.info("Video ID not found in any messages")

    # for message in messages:
    #     if video_id in message:
    #         logging.info(f"Found video ID in message: {message}")
    #         await telegrampart.send_picture(
    #             client, destination_chat_id, video_id, task_text
    #         )
    #         break
    # else:
    #     logging.info("Video ID not found in any messages")

    # await telegrampart.send_picture(client, destination_chat_id, video_id, task_text)


if __name__ == "__main__":
    # asyncio.run(main())
    client = TelegramClient("telegram", api_id, api_hash)

    with client:
        client.loop.run_until_complete(main())
