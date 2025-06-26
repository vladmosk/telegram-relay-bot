import asyncio
import nest_asyncio
from telethon import TelegramClient, events
from datetime import datetime, timedelta

nest_asyncio.apply()

api_id = 29873749
api_hash = 'f747a66e89ef4b31e6ca7b7d06445091'
session_file = 'session.session'
client = TelegramClient(session_file, api_id, api_hash)

target_chat_id = -1002712861852
source_chat = '@TOPOVHELP'

keywords = [
    '411', 'дача Ковалевского', 'люстдорфская', 'маяки', 'два столба', '2 столба',
    'Глушко', 'акварель 2', '2 акварель', 'переправа', 'черноморка', 'барабой',
    'малодолинское', 'великодолинское', 'малая долина', 'бп', 'блокпост', 'блок-пост',
    'леденци', 'леденцы', 'леденец', 'сухой лиман', 'прилиманское', 'новая долина',
    'доброалександровка', 'новогородковка', 'марьяновка', 'йосиповка',
    'петродолинское', 'петродолина', 'мирное', 'великий дальник', 'Вильямса',
    'таирова', 'ситицентр', 'сити центр', 'королева', 'ильфа и петрова',
    'фонтан', 'фантан', 'горького', 'талбухина', 'толбухина', 'тцк'
]

async def main():
    print("🚀 Запуск main()...")
    await client.start()
    print("📡 Бот подключен и слушает канал...")

    # --- Чтение сообщений за последний час ---
    async for message in client.iter_messages(source_chat, offset_date=datetime.now() - timedelta(hours=1)):
        if message.text and any(k in message.text.lower() for k in keywords):
            await client.send_message(target_chat_id, f'🔔 Старое сообщение (за час):\n\n{message.text}')

    @client.on(events.NewMessage(chats=source_chat))
    async def handler(event):
        if event.message.message and any(k in event.message.message.lower() for k in keywords):
            await client.send_message(target_chat_id, f'🔔 Новое сообщение:\n\n{event.message.message}')

    await client.run_until_disconnected()

asyncio.run(main())
