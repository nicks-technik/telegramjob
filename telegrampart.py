import os
import logging
from dotenv import load_dotenv
from telethon.sync import TelegramClient


async def send_picture(client, destination_chat_id, video_id, task_text):
    """
    Asynchronously sends a picture to a specified chat.

    Args:
        client: The Telegram client instance used to send the file.
        destination_chat_id (int or str): The ID or username of the destination chat.
        video_id (str): The ID of the video, used to locate the corresponding picture file.
        task_text (str): The caption text to be included with the picture.

    Returns:
        None
    """
    await client.send_file(
        destination_chat_id, "./png/" + video_id + ".png", caption=task_text
    )


async def scrape_message(client, channel, limit=50):
    """
    Scrape messages from a specified Telegram channel.

    This function uses an asynchronous Telegram client to iterate through messages
    in a given channel and collects the text of each message up to a specified limit.

    Args:
        client (TelegramClient): The Telegram client instance used to interact with the Telegram API.
        channel (str): The name or ID of the Telegram channel to scrape messages from.
        limit (int, optional): The maximum number of messages to scrape. Defaults to 50.

    Returns:
        list: A list of message texts scraped from the specified channel.
    """
    logging.info(f"Scraping messages from {channel}...")
    messages = []
    async for message in client.iter_messages(channel, limit=limit):
        if message.text:
            logging.debug(message.text)
            logging.debug("-" * 40)
            messages.append(message.text)
    return messages


async def main() -> None:
    """
    Main asynchronous function to interact with Telegram.

    This function performs the following tasks:
    1. Retrieves the list of dialogs (chats, groups, channels, etc.) associated with the client.
    2. Retrieves the client's own user information.
    3. Sends a message to the specified destination chat.
    4. Sends a file (image) to the specified destination chat with a caption.
    5. Sends a picture to the specified destination chat using a video ID.
    6. Scrapes messages from the specified source chat with a given limit and prints the result.

    Note:
    - Ensure that `client`, `destination_chat_id`, `send_picture`, `scrape_message`, and `source_chat_id` are defined and properly initialized before calling this function.
    """

    dialogs = await client.get_dialogs()

    me = await client.get_me()
    logging.debug(me.stringify())

    await client.send_message(destination_chat_id, "Hell, myself!")

    await client.send_file(
        destination_chat_id, "./png/NickTHorn.jpg", caption="Nick Thorn"
    )
    await send_picture(client, destination_chat_id, "3JZ_D3ELwOQ", "video_id")
    logging.info(await scrape_message(client, source_chat_id, limit=100))
    # client.run_until_disconnected()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    load_dotenv()

    api_id: int = int(os.getenv(key="ENV_API_ID"))
    api_hash: str = os.getenv(key="ENV_API_HASH")
    destination_chat_id: int = int(os.getenv("ENV_DESTINATION_CHAT_ID"))
    logging.info(f"Destination Chat ID: {destination_chat_id}")
    source_chat_id: int = int(os.getenv("ENV_SOURCE_CHAT_ID"))
    logging.info(f"Source Chat ID: {source_chat_id}")
    client = TelegramClient("telegram", api_id, api_hash)

    with client:
        client.loop.run_until_complete(main())
