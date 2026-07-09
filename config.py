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

# پامپ
PUMP_PERCENT = 10.0

# دامپ
DUMP_PERCENT = -10.0

# رشد از کف
MIN_RISE_FROM_LOW = 5.0

# حرکت غیرعادی
UNUSUAL_MOVE_PERCENT = 8.0

# هیجان بازار
FOMO_PERCENT = 15.0

# حجم غیرعادی
UNUSUAL_VOLUME_MULTIPLIER = 2.5

# حداقل امتیاز ارسال
MIN_SCORE = 80

# ===========================
# Resistance
# ===========================

FOUR_HOUR_RESISTANCE_DISTANCE = 2.0

DAILY_RESISTANCE_DISTANCE = 2.0

WEEKLY_RESISTANCE_DISTANCE = 5.0

THREE_DAY_RESISTANCE_DISTANCE = 3.0

# ===========================
# Support
# ===========================

SUPPORT_DISTANCE = 2.0

# ===========================
# Volume
# ===========================

VOLUME_MULTIPLIER = 2.0

# ===========================
# Cooldown
# ===========================

ALERT_COOLDOWN = 3600

# ===========================
# Alert Titles
# ===========================

ALERT_PUMP = "🚀 پامپ"

ALERT_DUMP = "📉 دامپ"

ALERT_FOMO = "🔥 هیجان بازار"

ALERT_UNUSUAL_MOVE = "⚡ حرکت غیرعادی"

ALERT_UNUSUAL_VOLUME = "📦 حجم غیرعادی"

ALERT_RESISTANCE = "⚠️ نزدیک مقاومت مهم"

ALERT_SUPPORT = "🟢 نزدیک حمایت"

ALERT_NORMAL = "📊 هشدار بازار"

# ===========================
# Score
# ===========================

SCORE_RISE = 30

SCORE_PUMP = 20

SCORE_RESISTANCE = 30

SCORE_VOLUME = 20

SCORE_FOMO = 25

SCORE_UNUSUAL = 20