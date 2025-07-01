import os
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import nest_asyncio

# Настройка логгера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
log = logging.getLogger("relay-bot")

# Разрешаем повторный запуск цикла
nest_asyncio.apply()
load_dotenv()

# Получение переменных окружения
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
SOURCE_CHAT_ID_RAW = os.getenv("SOURCE_CHAT_ID")

# Telegram клиент
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def main():
    await client.start()
    log.info("✅ Клиент подключен")

    # Получаем объект канала, чтобы избежать проблем с @username
    source_entity = await client.get_entity(SOURCE_CHAT_ID_RAW)
    log.info(f"📡 SOURCE_CHAT_ID entity получен: {source_entity.id}")

    # Подписка на события
    @client.on(events.NewMessage(chats=source_entity))
    async def handler(event):
        text = event.message.message
        if text:
            log.info(f"📥 Новое сообщение: {text[:80]}...")
            await client.send_message(TARGET_CHAT_ID, text)
            log.info(f"📤 Переслано в {TARGET_CHAT_ID}")

    log.info("🟢 Бот ожидает новые сообщения...")
    await client.run_until_disconnected()

# Запуск
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
