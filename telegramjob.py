import os
import logging
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
# destination_chat_id: str = os.getenv("ENV_SOURCE_CHAT_ID")


async def main() -> None:
    # run_telegram_bot()
    video_url = "https://www.youtube.com/watch?v=LNVXJUyaAhM"
    video_id = video_url.split("?v=")[1]
    task_text = "This is a test task"
    logging.info(f"Video ID: {video_id}")

    # creds = ytsubscribe.check_login()
    # if ytsubscribe.like_video(creds, video_id):
    #     channel_id = ytsubscribe.get_channel_id_from_video_id(creds, video_id)
    #     if ytsubscribe.subscribe_to_channel(creds, channel_id):
    #         logging.info(f"Successfully liked and subscribed to video: {video_id}")

    #         playwrightpart.process_youtube_video(video_id)
    await telegrampart.send_picture(client, destination_chat_id, video_id, task_text)


if __name__ == "__main__":
    # asyncio.run(main())
    client = TelegramClient("telegram", api_id, api_hash)

    with client:
        client.loop.run_until_complete(main())
