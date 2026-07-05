import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "60"))