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

# Поддержка повторного запуска
nest_asyncio.apply()

# Загрузка переменных окружения
load_dotenv()

# Конфигурация
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

# Обработка SOURCE_CHAT_ID
source = os.getenv("SOURCE_CHAT_ID")
SOURCE_CHAT_ID = source if source.startswith("@") else int(source)
log.info(f"🧾 SOURCE_CHAT_ID: {SOURCE_CHAT_ID}")

# Обработка TARGET_CHAT_ID
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
log.info(f"🧾 TARGET_CHAT_ID: {TARGET_CHAT_ID}")

# Основной запуск
async def main():
    log.info("🚀 Запуск main()...")
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()
    log.info("📡 Бот подключен и слушает канал...")

    @client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
    async def handler(event):
        text = event.message.message
        log.info(f"📥 Получено сообщение: {text}")
        if text:
            await client.send_message(TARGET_CHAT_ID, text)
            log.info(f"📤 Переслано сообщение в {TARGET_CHAT_ID}")

    await client.run_until_disconnected()

# Запуск
asyncio.run(main())
