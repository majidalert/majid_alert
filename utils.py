from datetime import datetime


def format_number(value):
    try:
        value = float(value)

        if value >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"

        if value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"

        if value >= 1_000:
            return f"{value/1_000:.2f}K"

        return f"{value:.4f}"

    except:
        return str(value)


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def make_message(title, symbol, price, change, volume, score):

    return (
        f"🚨 MAJID ALERT AI\n\n"
        f"{title}\n\n"
        f"🪙 ارز: {symbol}\n"
        f"💰 قیمت: {price}\n"
        f"📈 تغییر: {change:.2f}%\n"
        f"📦 حجم: {format_number(volume)}\n"
        f"⭐ امتیاز: {score}/100\n"
        f"🕒 {now()}"
    )