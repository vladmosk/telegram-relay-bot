async def main():
    log.info("🚀 Запуск main()...")
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
    await client.start()

    source_username = os.getenv("SOURCE_CHAT_ID")
    source_entity = await client.get_entity(source_username)
    log.info(f"✅ SOURCE_CHAT_ID resolved to entity: {source_entity.id}")

    log.info("📡 Чтение последних сообщений через iter_messages...")

    async for msg in client.iter_messages(source_entity, limit=5):
        if msg.text:
            log.info(f"📥 Найдено сообщение: {msg.text[:100]}")
            await client.send_message(TARGET_CHAT_ID, msg.text)
            log.info(f"📤 Переслано в {TARGET_CHAT_ID}")

    log.info("🕓 Завершен просмотр 5 сообщений. Переходим в ожидание...")
    await client.run_until_disconnected()
