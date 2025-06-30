import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import nest_asyncio
import logging

# Настраиваем логгер
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger("relay-bot")


# Поддержка повторного запуска (например, в Jupyter)
nest_asyncio.apply()

# Загружаем переменные окружения
load_dotenv()

# Конфигурация из .env
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
SOURCE_CHAT = os.getenv("SOURCE_CHAT")  # @канал или ID
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

# Клиент через StringSession
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

CATEGORIES = {
    "411 🏡": [
        '411', 'дача Ковалевского', 'люстдорфская', 'Глушко', 'акварель 2', '2 акварель',
        'черноморка', 'Вильямса', 'таирова', 'ильфа и петрова', 'ситицентр', 'сити центр', 'королева'
    ],
    "Рыбалка 🎣 через 2 столба": [
        'маяки', 'два столба', '2 столба', 'авангард', 'сухой лиман', 'дальник',
        'хлебодарское', 'расселенец', 'мирное', 'беляевка'
    ],
    "Рыбалка 🎣 петродолина": [
        'переправа', 'барабой', 'малодолинское', 'великодолинское', 'малая долина', 'прилиманское',
        'новая долина', 'доброалександровка', 'новогородковка', 'марьяновка', 'йосиповка',
        'петродолинское', 'петродолина'
    ],
    "🚨 Внимание!": [
        'менты', 'тормозят', 'планшет', 'беляевка', 'люстра', 'люстре', 'бп', 'блокпост',
        'блок-пост', 'леденци', 'леденцы', 'леденец'
    ],
    "🌳 Центр и парки": [
        'фонтан', 'фантан', 'горького', 'талбухина', 'толбухина', 'парк победы'
    ],
    "ЖД 🚉": [
        'жд'
    ]
}


def detect_category(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    return "🔔 Новое сообщение"

# Основной запуск
async def main():
    log.info("🚀 Запуск main()...")
    await client.start()
    log.info("📡 Бот подключен и слушает канал...")

    @client.on(events.NewMessage(chats=SOURCE_CHAT))
    async def handler(event):
        text = event.message.message
        if text:
            prefix = detect_category(text)
            final_message = f"{prefix}:\n\n{text}"
            await client.send_message(TARGET_CHAT_ID, final_message)

    await client.run_until_disconnected()

# Запуск
asyncio.run(main())
