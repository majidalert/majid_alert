import os

# ==========================================
# Telegram
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ==========================================
# Scanner
# ==========================================

SCAN_INTERVAL = int(
    os.getenv("SCAN_INTERVAL", "60")
)

# ==========================================
# Bybit
# ==========================================

BASE_URL = "https://api.bybit.com"

# ==========================================
# Pump / Dump
# ==========================================

PUMP_PERCENT = 10.0
DUMP_PERCENT = -10.0

UNUSUAL_MOVE_PERCENT = 8.0
FOMO_PERCENT = 15.0

# ==========================================
# رشد از کف
# ==========================================

MIN_RISE_FROM_LOW = 5.0

# حداقل درصد مسیر طی شده
# تا مقاومت
# (جایگزین شرط ثابت 30 درصد)

MIN_EXTENSION_PERCENT = 75.0

# ==========================================
# مقاومت ها
# ==========================================

FOUR_HOUR_RESISTANCE_DISTANCE = 2.0

DAILY_RESISTANCE_DISTANCE = 2.0

THREE_DAY_RESISTANCE_DISTANCE = 3.0

WEEKLY_RESISTANCE_DISTANCE = 5.0

# ==========================================
# شکست مقاومت
# ==========================================

BREAKOUT_CONFIRM_PERCENT = 0.40

PULLBACK_DISTANCE = 0.50

# ==========================================
# حجم
# ==========================================

VOLUME_MULTIPLIER = 2.0

UNUSUAL_VOLUME_MULTIPLIER = 2.5

# ==========================================
# امتیازها
# ==========================================

MIN_SCORE = 80

MIN_MULTITRADE_SCORE = 80

SCORE_EXTENSION = 30

SCORE_RISE = 20

SCORE_VOLUME = 15

SCORE_PUMP = 15

SCORE_4H = 10

SCORE_1D = 15

SCORE_3D = 20

SCORE_1W = 30

SCORE_BREAKOUT = 20

SCORE_PULLBACK = 15

# ==========================================
# احتمال ها
# ==========================================

MAX_CORRECTION_PROBABILITY = 90

MIN_CORRECTION_PROBABILITY = 55

# ==========================================
# هشدار تکراری
# ==========================================

ALERT_COOLDOWN = 3600

# ==========================================
# عناوین
# ==========================================

ALERT_SHORT = "🟥 SHORT MULTITRADE SETUP"

ALERT_BREAKOUT = "🚀 BREAKOUT"

ALERT_PULLBACK = "🔄 PULLBACK"

ALERT_PUMP = "🚀 PUMP"

ALERT_DUMP = "📉 DUMP"