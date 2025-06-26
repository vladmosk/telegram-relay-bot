from telethon.sync import TelegramClient

# Используй те же api_id и api_hash
api_id = 29873749
api_hash = 'f747a66e89ef4b31e6ca7b7d06445091'

# Название сессии — любое, но оно должно совпадать с тем, через который логинишься (пусть будет 'session')
with TelegramClient('session', api_id, api_hash) as client:
    dialogs = client.get_dialogs()
    print("📋 Доступные чаты и каналы:\n")
    for dialog in dialogs:
        name = getattr(dialog.entity, 'title', getattr(dialog.entity, 'first_name', 'Нет имени'))
        chat_id = dialog.entity.id
        print(f'{name}: {chat_id}')
