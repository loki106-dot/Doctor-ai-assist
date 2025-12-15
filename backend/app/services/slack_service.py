import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_message(text: str):
    if not SLACK_WEBHOOK_URL:
        print("❌ SLACK_WEBHOOK_URL not set")
        return

    payload = {
        "text": text
    }

    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code != 200:
        print("❌ Slack error:", response.text)
    else:
        print("✅ Slack message sent")
