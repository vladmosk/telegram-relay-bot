import asyncio
import nest_asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

# Поддержка повторного запуска (например, в Jupyter)
nest_asyncio.apply()

# Загружаем переменные окружения
load_dotenv()

# Конфигурация
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
session_file = 'session.session'
client = TelegramClient("/mnt/data/session", api_id, api_hash)

# Чаты
target_chat_id = -1002712861852
source_chat = '@TOPOVHELP'

# Категории и ключевые слова
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
    print("🚀 Запуск main()...")
    await client.start()
    print("📡 Бот подключен и слушает канал...")

    @client.on(events.NewMessage(chats=source_chat))
    async def handler(event):
        text = event.message.message
        if text:
            prefix = detect_category(text)
            final_message = f"{prefix}:\n\n{text}"
            await client.send_message(target_chat_id, final_message)

    await client.run_until_disconnected()

# Запуск
asyncio.run(main())
