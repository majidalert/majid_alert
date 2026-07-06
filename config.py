import os

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Scanner
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "60"))

# Bybit API
BASE_URL = "https://api.bybit.com"

# Alert Settings
PUMP_PERCENT = 10.0
DUMP_PERCENT = -10.0

# فاصله تا سقف قبلی
NEAR_HIGH_PERCENT = 2.0

# حجم غیرعادی
VOLUME_MULTIPLIER = 2.0

# جلوگیری از هشدار تکراری
ALERT_COOLDOWN = 3600