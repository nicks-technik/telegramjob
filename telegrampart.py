import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
import asyncio

load_dotenv()

api_id: int = int(os.getenv(key="ENV_API_ID"))
api_hash: str = os.getenv(key="ENV_API_HASH")
destination_chat_id: int = int(os.getenv("ENV_DESTINATION_CHAT_ID"))
# destination_chat_id: str = os.getenv("ENV_SOURCE_CHAT_ID")

client = TelegramClient("telegram", api_id, api_hash)


async def main():
    # with TelegramClient("name", api_id, api_hash) as client:
    me = await client.get_me()
    print(me.stringify())

    await client.send_message(destination_chat_id, "Hellx, myself!")
    # client.send_message("me", "Hello, myself!")
    # print(client.download_profile_photo("me"))

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:

    # @client.on(events.NewMessage(pattern="(?i).*Mission Nr."))
    # async def handler(event):
    # await event.reply("Hey!")
    await client.send_file(destination_chat_id, "./NickTHorn.jpg", caption="Nick Thorn")

    client.run_until_disconnected()


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
