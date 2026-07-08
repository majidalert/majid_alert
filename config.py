import os

# ==========================
# Telegram
# ==========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ==========================
# Scanner
# ==========================

SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "60"))

# ==========================
# Bybit API
# ==========================

BASE_URL = "https://api.bybit.com"

# ==========================
# Pump / Dump
# ==========================

PUMP_PERCENT = 10.0
DUMP_PERCENT = -10.0

# ==========================
# Resistance
# ==========================

# فاصله تا مقاومت روزانه
DAILY_RESISTANCE_DISTANCE = 2.0

# فاصله تا مقاومت هفتگی
WEEKLY_RESISTANCE_DISTANCE = 3.0

# فاصله تا حمایت
SUPPORT_DISTANCE = 2.0

# ==========================
# Psychological Numbers
# ==========================

# فاصله مجاز تا عدد روانی
PSYCHOLOGICAL_DISTANCE = 1.0

# ==========================
# Volume
# ==========================

# حجم غیرعادی
VOLUME_MULTIPLIER = 2.0

# ==========================
# Trend
# ==========================

EMA_FAST = 20
EMA_SLOW = 50

RSI_PERIOD = 14

# ==========================
# Alert Score
# ==========================

MIN_SCORE = 60

HIGH_SCORE = 80

# ==========================
# Alert Cooldown
# ==========================

ALERT_COOLDOWN = 3600

# ==========================
#