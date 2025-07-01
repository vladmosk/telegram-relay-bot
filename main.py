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
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

# Жёстко указываем нужный канал: ТОТ САМЫЙ — ТОПОВХЕЛП
SOURCE_CHANNEL_ID = -1002050105527

# Создание клиента
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def setup():
    await client.start()
    log.info("✅ Клиент успешно запущен")
    log.info(f"📡 Слушаем только канал ID: {SOURCE_CHANNEL_ID}")
    log.info("🟢 Бот работает, ожидает новые сообщения...")

    @client.on(events.NewMessage)
    async def handler(event):
        if event.chat_id != SOURCE_CHANNEL_ID:
            return  # игнорируем всё, кроме нужного канала

        text = event.message.message
        if text:
            log.info(f"📥 Получено сообщение: {text[:80]}")
            await client.send_message(TARGET_CHAT_ID, text)
            log.info(f"📤 Переслано сообщение в {TARGET_CHAT_ID}")

    await client.run_until_disconnected()

# Запуск
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())
