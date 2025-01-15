import os
from dotenv import load_dotenv
from telethon.sync import TelegramClient

import asyncio


async def send_picture(client, destination_chat_id, video_id, task_text):
    await client.send_file(
        destination_chat_id, "./png/" + video_id + ".png", caption=task_text
    )


async def scrape_message(client, channel, limit=50):
    print(f"Scraping messages from {channel}...")
    messages = []
    async for message in client.iter_messages(channel, limit=limit):
        if message.text:
            print(message.text)
            print("-" * 40)
            print("=" * 40)
            print("-" * 40)
            messages.append(message.text)
    return messages


async def main():

    dialogs = await client.get_dialogs()

    # with TelegramClient("name", api_id, api_hash) as client:
    me = await client.get_me()
    print(me.stringify())

    await client.send_message(destination_chat_id, "Hell, myself!")
    # client.send_message("me", "Hello, myself!")
    # print(client.download_profile_photo("me"))

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:

    # @client.on(events.NewMessage(pattern="(?i).*Mission Nr."))
    # async def handler(event):
    # await event.reply("Hey!")

    await client.send_file(
        destination_chat_id, "./png/NickTHorn.jpg", caption="Nick Thorn"
    )
    await send_picture(client, destination_chat_id, "3JZ_D3ELwOQ", "video_id")
    print(await scrape_message(client, source_chat_id, limit=120))
    # client.run_until_disconnected()


if __name__ == "__main__":
    load_dotenv()

    api_id: int = int(os.getenv(key="ENV_API_ID"))
    api_hash: str = os.getenv(key="ENV_API_HASH")
    destination_chat_id: int = int(os.getenv("ENV_DESTINATION_CHAT_ID"))
    # print(f"Destination Chat ID: {destination_chat_id}")
    source_chat_id: int = int(os.getenv("ENV_SOURCE_CHAT_ID"))
    print(f"Source Chat ID: {source_chat_id}")
    client = TelegramClient("telegram", api_id, api_hash)

    with client:
        client.loop.run_until_complete(main())
