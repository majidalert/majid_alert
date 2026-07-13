import os

# ==========================================
# Telegram
# ==========================================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = os.environ.get("CHAT_ID", "")

# ==========================================
# Scanner
# ==========================================

SCAN_INTERVAL = int(os.environ.get("SCAN_INTERVAL", "60"))

# ==========================================
# Alert Control
# ==========================================

ALERT_COOLDOWN = int(os.environ.get("ALERT_COOLDOWN", "3600"))

# ==========================================
# Bybit
# ==========================================

BASE_URL = "https://api.bybit.com"

# ==========================================
# Pump / Dump
# ==========================================

PUMP_PERCENT = 8.0
DUMP_PERCENT = -8.0

# نام‌های قدیمی برای سازگاری
PUMP_THRESHOLD = PUMP_PERCENT
DUMP_THRESHOLD = abs(DUMP_PERCENT)

UNUSUAL_MOVE_PERCENT = 6.0
FOMO_PERCENT = 12.0

# ==========================================
# رشد از کف
# ==========================================

MIN_RISE_FROM_LOW = 3.0
MIN_EXTENSION_PERCENT = 60.0

# ==========================================
# MultiTrade / Resistance
# ==========================================

RESISTANCE_DISTANCE_PERCENT = 3.5

# سازگاری با نسخه‌های مختلف اسکنر
FOUR_HOUR_RESISTANCE_DISTANCE = 3.5
DAILY_RESISTANCE_DISTANCE = 3.5
THREE_DAY_RESISTANCE_DISTANCE = 3.5
WEEKLY_RESISTANCE_DISTANCE = 3.5

MIN_SIGNAL_SCORE = 70
SIGNAL_SCORE = MIN_SIGNAL_SCORE
SCORE_THRESHOLD = MIN_SIGNAL_SCORE

# ==========================================
# Volume Detection
# ==========================================

VOLUME_SPIKE_MULTIPLIER = 2.0

# سازگاری با نسخه‌های مختلف
VOLUME_MULTIPLIER = VOLUME_SPIKE_MULTIPLIER

# ==========================================
# Trend Filter
# ==========================================

WEEKLY_GROWTH_ALERT = 50.0
ATH_DISTANCE_ALERT = 5.0

# ==========================================
# Risk Control
# ==========================================

MAX_ALERTS_PER_SCAN = 10