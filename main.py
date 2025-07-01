import os
import logging
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import nest_asyncio

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger("relay-bot")

# Повторное использование event loop
nest_asyncio.apply()
load_dotenv()

# Переменные окружения
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
SOURCE_CHAT_ID = os.getenv("SOURCE_CHAT_ID")  # Например: @TOPOVHELP
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))  # Например: -100...

# Создание клиента
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def setup():
    await client.start()
    log.info("✅ Клиент успешно запущен")

    source_entity = await client.get_entity(SOURCE_CHAT_ID)
    source_id = source_entity.id
    log.info(f"📡 SOURCE_CHAT_ID entity: {source_id}")

    @client.on(events.NewMessage)
    async def handler(event):
        text = event.message.message
        chat_id = event.chat_id
        if text:
            log.info(f"⚡ Поймано сообщение из {chat_id}: {text[:80]}")
            if str(chat_id) == str(source_id) or str(chat_id).endswith(str(source_id)):
                await client.send_message(TARGET_CHAT_ID, text)
                log.info(f"📤 Переслано сообщение в {TARGET_CHAT_ID}")

    log.info("🟢 Бот работает, ожидает новые сообщения...")
    await client.run_until_disconnected()

# Запуск
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())
