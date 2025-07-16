import os
import requests

def send_discord(message):
    webhook = os.getenv("DISCORD_WEBHOOK")
    if not webhook:
        print("Discord webhook not set")
        return
    data = {"content": message}
    try:
        r = requests.post(webhook, json=data)
        if r.status_code != 204:
            print(f"Discord webhook error: {r.status_code} {r.text}")
    except Exception as e:
        print("Discord notification error:", e)
