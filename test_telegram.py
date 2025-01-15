import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

print(f"Bot Token: {TOKEN}")
print(f"Source Chat ID: {SOURCE_CHAT_ID}")
print(f"Destination Chat ID: {DESTINATION_CHAT_ID}")
print(f"Specific Text: {SPECIFIC_TEXT}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token("TOKEN").build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
