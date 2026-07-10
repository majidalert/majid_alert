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

# حداقل رشد از کف
MIN_RISE_FROM_LOW = 5.0

# حداقل درصد طی شدن مسیر تا مقاومت اصلی
MIN_EXTENSION_PERCENT = 75.0

# حرکت غیرعادی
UNUSUAL_MOVE_PERCENT = 8.0

# هیجان بازار
FOMO_PERCENT = 15.0

# حجم غیرعادی
UNUSUAL_VOLUME_MULTIPLIER = 2.5

# حداقل امتیاز ارسال
MIN_SCORE = 80

# حداقل امتیاز مولتی ترید
MIN_MULTITRADE_SCORE = 80

# ===========================
# Resistance
# ===========================

FOUR_HOUR_RESISTANCE_DISTANCE = 2.0

DAILY_RESISTANCE_DISTANCE = 2.0

THREE_DAY_RESISTANCE_DISTANCE = 3.0

WEEKLY_RESISTANCE_DISTANCE = 5.0

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

SCORE_RISE = 20

SCORE_EXTENSION = 20

SCORE_VOLUME = 10

SCORE_PUMP = 10

SCORE_BREAKOUT = 10

SCORE_PULLBACK = 10

SCORE_4H = 15

SCORE_1D = 20

SCORE_3D = 25

SCORE_1W = 30