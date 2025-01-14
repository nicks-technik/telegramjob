from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()

TOKEN: str = os.getenv(key="TELEGRAM_BOT_TOKEN")
SOURCE_CHAT_ID = os.getenv(key="SOURCE_CHAT_ID")
DESTINATION_CHAT_ID = os.getenv(key="DESTINATION_CHAT_ID")
SPECIFIC_TEXT: str = os.getenv(key="SPECIFIC_TEXT", default="video link")

if not TOKEN:
    raise Exception("TELEGRAM_BOT_TOKEN not found in environment variables")

if not SOURCE_CHAT_ID:
    raise Exception("SOURCE_CHAT_ID not found in environment variables")
else:
    SOURCE_CHAT_ID = int(SOURCE_CHAT_ID)

if not DESTINATION_CHAT_ID:
    raise Exception("DESTINATION_CHAT_ID not found in environment variables")
else:
    DESTINATION_CHAT_ID = int(DESTINATION_CHAT_ID)

print(f"Bot Token: {TOKEN}")
print(f"Source Chat ID: {SOURCE_CHAT_ID}")
print(f"Destination Chat ID: {DESTINATION_CHAT_ID}")
print(f"Specific Text: {SPECIFIC_TEXT}")


async def message_handler(update: Update):
    """
    Handle incoming messages from Telegram updates.

    Args:
        update (Update): The incoming update from Telegram

    Returns:
        None
    """
    if update.effective_chat.id == SOURCE_CHAT_ID:
        message = update.message
        if message and message.text and SPECIFIC_TEXT in message.text:
            print(message.text)


def run_telegram_bot() -> None:
    """
    Initializes and runs a Telegram bot using the python-telegram-bot library.

    This function performs the following steps:
    1. Creates a new Application instance using the bot TOKEN
    2. Adds a message handler that processes all text messages
    3. Starts the bot in polling mode

    The bot will continue running and processing messages until the program is terminated.

    Returns:
        None
    """
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, message_handler))
    app.run_polling()


if __name__ == "__main__":
    run_telegram_bot()
