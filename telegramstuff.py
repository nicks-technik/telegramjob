from logger_config import logger

from telethon.sync import TelegramClient
from config import Config


async def send_picture(client, destination_chat_id, filename: str, caption: str) -> bool:
    """
    Asynchronously sends a picture to a specified chat.

    Args:
        client: The Telegram client instance used to send the file.
        destination_chat_id (int or str): The ID or username of the destination chat.
        filename (str): The path to the file to send.
        caption (str): The caption for the picture.

    Returns:
        bool: True if the picture was sent successfully, False otherwise.

    """
    for i in range(2):
        try:
            await client.send_file(
                destination_chat_id, f"./png/{filename}", caption=caption
            )

            logger.info(
                f"Screenshot sent: {filename} to {destination_chat_id}"
            )
            return True
            # only the last received job should be executed
            break
        except Exception as e:
            logger.error(f"Error sending screenshot {filename}: {e}")
    return False


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
    logger.info(f"Scraping messages from {channel}...")
    messages = []
    async for message in client.iter_messages(channel, limit=limit):
        if message.text:
            logger.debug(message.text)
            logger.debug("-" * 40)
            messages.append(message.text)
    return messages
