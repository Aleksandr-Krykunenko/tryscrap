import os
import requests
from telethon import TelegramClient, events

# Дані беруться з налаштувань Railway (Environment Variables)
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')
source_channel = os.environ.get('SOURCE_CHANNEL')
n8n_webhook_url = os.environ.get('N8N_WEBHOOK_URL')

client = TelegramClient(None, api_id, api_hash).start(phone=lambda: os.environ.get('PHONE'))

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    if event.raw_text:
        # Відправка даних в n8n
        data = {"text": event.raw_text}
        try:
            requests.post(n8n_webhook_url, json=data)
            print(f"Sent to n8n: {event.raw_text[:30]}...")
        except Exception as e:
            print(f"Error: {e}")

print("UserBot is running...")
client.run_until_disconnected()
