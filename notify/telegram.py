import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram bot token or chat id not set")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        r = requests.get(url, params=params)
        if r.status_code != 200:
            print(f"Telegram send error: {r.status_code} {r.text}")
    except Exception as e:
        print("Telegram notification error:", e)
