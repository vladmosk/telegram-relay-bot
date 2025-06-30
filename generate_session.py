from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("Введите API_ID: "))
api_hash = input("Введите API_HASH: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("✅ Успешно вошли в Telegram")
    print("🔑 Ваша строка StringSession:")
    print(client.session.save())
