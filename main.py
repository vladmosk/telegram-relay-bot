import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import nest_asyncio
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger("relay-bot")

nest_asyncio.apply()
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

# Основной запуск
async def main():
    log.info("🚀 Запуск main()...")
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()

    # Получаем entity канала явно
    source_username = os.getenv("SOURCE_CHAT_ID")
    source_entity = await client.get_entity(source_username)
    log.info(f"✅ SOURCE_CHAT_ID resolved to entity: {source_entity.id}")

    log.info("📡 Бот подключен и слушает канал...")

    @client.on(events.NewMessage(chats=source_entity))
    async def handler(event):
        text = event.message.message
        log.info(f"📥 Получено сообщение: {text}")
        if text:
            await client.send_message(TARGET_CHAT_ID, text)
            log.info(f"📤 Переслано сообщение в {TARGET_CHAT_ID}")

    await client.run_until_disconnected()

asyncio.run(main())
