from telethon.sync import TelegramClient, events
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
channel_from = os.getenv("CHANNEL_FROM")
channel_to = os.getenv("CHANNEL_TO")

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_from))
async def handler(event):
    await client.send_message(channel_to, event.message)

client.start()
client.run_until_disconnected()
