from telethon.sync import TelegramClient

api_id = 29873749
api_hash = 'f747a66e89ef4b31e6ca7b7d06445091'

with TelegramClient('session', api_id, api_hash) as client:
    print("✅ Успешный вход как:", client.get_me().first_name)
