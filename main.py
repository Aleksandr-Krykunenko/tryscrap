import os
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Отримуємо змінні з налаштувань Railway
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')
source_channel = os.environ.get('SOURCE_CHANNEL')
n8n_webhook_url = os.environ.get('N8N_WEBHOOK_URL')

# Запуск через StringSession (це позбавить від помилки з номером телефону)
client = TelegramClient(StringSession(session_string), api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.raw_text:
        data = {"text": event.raw_text}
        try:
            requests.post(n8n_webhook_url, json=data)
            print("Повідомлення відправлено в n8n")
        except Exception as e:
            print(f"Помилка: {e}")

print("Юзербот активований і слухає канал...")
client.start()
client.run_until_disconnected()
