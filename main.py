import asyncio
import nest_asyncio
from telethon import TelegramClient, events

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
    'фонтан', 'фантан', 'горького', 'талбухина', 'толбухина', 'менты', 'тормозят', 'планшет', 'беляевка', 'люстра', 'люстре'
]

async def main():
    print("🚀 Запуск main()...")
    await client.start()
    print("📡 Бот подключен и слушает канал...")

    @client.on(events.NewMessage(chats=source_chat))
    async def handler(event):
        text = event.message.message
        if text and any(k in text.lower() for k in keywords):
            await client.send_message(target_chat_id, f'🔔 Новое сообщение:\n\n{text}')

    await client.run_until_disconnected()

asyncio.run(main())
