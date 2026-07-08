import os

# ===========================
# Telegram
# ===========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ===========================
# Scanner
# ===========================

SCAN_INTERVAL = int(
    os.getenv("SCAN_INTERVAL", "60")
)

# ===========================
# Bybit
# ===========================

BASE_URL = "https://api.bybit.com"

# ===========================
# Alert Settings
# ===========================

PUMP_PERCENT = 10.0

DUMP_PERCENT = -10.0

# حداقل رشد از کف
MIN_RISE_FROM_LOW = 50.0

# حداقل امتیاز برای هشدار
MIN_SCORE = 60

# ===========================
# مقاومت ها
# ===========================

# فاصله تا مقاومت روزانه
DAILY_RESISTANCE_DISTANCE = 2.0

# فاصله تا مقاومت ۳ روزه
THREE_DAY_RESISTANCE_DISTANCE = 3.0

# فاصله تا مقاومت هفتگی
WEEKLY_RESISTANCE_DISTANCE = 5.0

# ===========================
# حجم
# ===========================

VOLUME_MULTIPLIER = 2.0

# ===========================
# جلوگیری از هشدار تکراری
# ===========================

ALERT_COOLDOWN = 3600