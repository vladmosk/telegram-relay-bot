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

nest_asyncio.apply()
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

# Жёстко указываем ID канала @TOPOVHELP
SOURCE_CHANNEL_ID = -1002050105527

# Категории и ключевые слова
CATEGORIES = {
    "411 🏡": [
        '411', 'дача Ковалевского', 'черноморка', 'очистн', 'гогол', 'демченк', 'отважн', 'орехов', 'авиньен', 'долг', 'архитекторск', 'авиньён'
    ],
    "Кадор 💼 🏋️": [
        'акварель 2', '2 акварель', 'маршал сити', 'кадор', 'жемчужин', 'маршала жукова', 'небесн'
    ],
    "Таирова 🌃": [
        'люстдорфск', 'глушко', 'вильямс', 'таиров', 'ильфа и петрова', 'глода', 'ситик', 'ситицентр', 'сити центр', 'королев', 'клюшк', 'привал', 'южн', 'киевск', 'львовск', 'левитан', 'костанд', 'риф'
    ],
    "🌳 Парк Горького": [
        'горьког', 'инглез', 'варненск', 'космонавт', 'терешков', 'генерала петрова', 'гайдар'
    ],
    "Рыбалка 🎣 через 2 столба": [
        'маяки', 'два столба', '2 столба', 'авангард', 'сухой лиман', 'дальник', 'хлебодарск', 'расселенец', 'мирн', 'беляевк', 'рени', 'измаил'
    ],
    "Рыбалка 🎣 петродолина": [
        'переправ', 'барабой', 'малодолинск', 'великодолинск', 'малая долин', 'большая долин', 'прилиманск', 'новая долин', 'доброалександровк', 'новогородковк', 'марьяновк', 'йосиповк', 'петродолинск', 'петродолин'
    ],
    "👮 Внимание!": [
        'мент', 'тормоз', 'планшет', 'люстр', 'бп', 'блокпост', 'блок-пост', 'леденц', 'патруль', 'останавлив'
    ],
    "🚨 БП": [
        'бп', 'блокпост', 'блок-пост'
    ],
    "⛲️ Фонтан": [
        'фонтан', 'фантан', 'горьког', 'бухин', 'толбухин', 'талбухин', 'парк побед', 'побед', 'адмиральск', 'говоров', 'сегедск'
    ],
    "ЖД 🚉": [
        r'\bжд\b', 'среднефонтанск', 'водопроводн'
    ]
}


# Функция для определения категории по ключевым словам
def detect_category(text: str) -> str | None:
    text_lower = text.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    return None

# Telegram клиент
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
        if not text:
            return  # игнорируем пустые сообщения

        category = detect_category(text)
        if not category:
            log.info("🔕 Пропущено сообщение без категории")
            return  # если нет ключевых слов — пропускаем

        final_text = f"{category}:\n\n{text}"
        await client.send_message(TARGET_CHAT_ID, final_text)
        log.info(f"📤 Переслано сообщение в {TARGET_CHAT_ID} с категорией: {category}")

    await client.run_until_disconnected()

# Запуск
loop = asyncio.get_event_loop()
loop.run_until_complete(setup())
