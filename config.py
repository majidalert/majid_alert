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


# حداقل رشد از کف 24 ساعته
# کاهش داده شد تا فرصت های بیشتری پیدا شوند

MIN_RISE_FROM_LOW = 5.0


# حداقل امتیاز هشدار

MIN_SCORE = 60



# ===========================
# مقاومت ها
# ===========================

# فاصله قیمت تا مقاومت 4 ساعته

FOUR_HOUR_RESISTANCE_DISTANCE = 2.0


# فاصله قیمت تا مقاومت روزانه

DAILY_RESISTANCE_DISTANCE = 2.0


# فاصله قیمت تا مقاومت هفتگی

WEEKLY_RESISTANCE_DISTANCE = 5.0


# فاصله قیمت تا مقاومت 3 روزه

THREE_DAY_RESISTANCE_DISTANCE = 3.0



# ===========================
# حجم
# ===========================

VOLUME_MULTIPLIER = 2.0



# ===========================
# جلوگیری از هشدار تکراری
# ===========================

ALERT_COOLDOWN = 3600