import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import nest_asyncio
import logging
import asyncio

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger("relay-bot")

# Разрешаем повторный запуск loop
nest_asyncio.apply()

# Загрузка переменных
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
SOURCE_CHAT_ID = os.getenv("SOURCE_CHAT_ID")

# Создаём клиент
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def setup():
    await client.start()
    source_entity = await client.get_entity(SOURCE_CHAT_ID)
    log.info(f"✅ SOURCE_CHAT_ID resolved to entity: {source_entity.id}")

    log.info("📡 Чтение последних сообщений через iter_messages...")

    async for msg in client.iter_messages(source_entity, limit=5):
        if msg.text:
            log.info(f"📥 Найдено сообщение: {msg.text[:100]}")
            await client.send_message(TARGET_CHAT_ID, msg.text)
            log.info(f"📤 Переслано в {TARGET_CHAT_ID}")

    log.info("🕓 Переходим в ожидание...")
    @client.on(events.NewMessage(chats=source_entity))
    async def handler(event):
        text = event.message.message
        log.info(f"📥 Получено сообщение: {text}")
        if text:
            await client.send_message(TARGET_CHAT_ID, text)
            log.info(f"📤 Переслано сообщение в {TARGET_CHAT_ID}")

    await client.run_until_disconnected()

# Запуск без asyncio.run()
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())
