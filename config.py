import os


# ==========================================
# Telegram
# ==========================================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")


# ==========================================
# Scanner
# ==========================================

SCAN_INTERVAL = int(
    os.environ.get("SCAN_INTERVAL", "60")
)


# ==========================================
# Bybit
# ==========================================

BASE_URL = "https://api.bybit.com"


# ==========================================
# Alert Control
# ==========================================

ALERT_COOLDOWN = 1800


# ==========================================
# Pump / Dump
# ==========================================

PUMP_PERCENT = 8.0
DUMP_PERCENT = -8.0

# سازگاری با نسخه‌های مختلف اسکنر
PUMP_THRESHOLD = PUMP_PERCENT
DUMP_THRESHOLD = abs(DUMP_PERCENT)

UNUSUAL_MOVE_PERCENT = 6.0
FOMO_PERCENT = 12.0


# ==========================================
# رشد از کف
# ==========================================

MIN_RISE_FROM_LOW = 3.0

# درصد مسیر طی شده تا مقاومت
MIN_EXTENSION_PERCENT = 60.0


# ==========================================
# Resistance Detection
# ==========================================

FOUR_HOUR_RESISTANCE_DISTANCE = 3.0
DAILY_RESISTANCE_DISTANCE = 3.0
THREE_DAY_RESISTANCE_DISTANCE = 4.0
WEEKLY_RESISTANCE_DISTANCE = 6.0

# نام عمومی برای نسخه‌های قدیمی
RESISTANCE_DISTANCE_PERCENT = 3.0


# ==========================================
# Breakout / Pullback
# ==========================================

BREAKOUT_CONFIRM_PERCENT = 0.30
PULLBACK_DISTANCE = 0.80


# ==========================================
# Volume Detection
# ==========================================

VOLUME_MULTIPLIER = 1.5

# سازگاری با نسخه‌های قبلی
VOLUME_SPIKE_MULTIPLIER = 2.0
UNUSUAL_VOLUME_MULTIPLIER = 2.0


# ==========================================
# Score System
# ==========================================

MIN_SCORE = 70
MIN_SIGNAL_SCORE = 70
MIN_MULTITRADE_SCORE = 70

SCORE_THRESHOLD = 70
SIGNAL_SCORE = 70

SCORE_EXTENSION = 20
SCORE_RISE = 15
SCORE_VOLUME = 10
SCORE_PUMP = 10

SCORE_4H = 20
SCORE_1D = 20
SCORE_3D = 25
SCORE_1W = 30

SCORE_BREAKOUT = 15
SCORE_PULLBACK = 10


# ==========================================
# Probability
# ==========================================

MAX_CORRECTION_PROBABILITY = 85
MIN_CORRECTION_PROBABILITY = 55


# ==========================================
# Alert Labels
# ==========================================

ALERT_SHORT = "🟥 SHORT"
ALERT_LONG = "🟩 LONG"

ALERT_PUMP = "🚀 PUMP"
ALERT_DUMP = "🔻 DUMP"

ALERT_VOLUME = "📊 VOLUME SPIKE"
ALERT_BREAKOUT = "🚀 BREAKOUT"
ALERT_PULLBACK = "🔄 PULLBACK"


# ==========================================
# Risk Control
# ==========================================

MAX_ALERTS_PER_SCAN = 10