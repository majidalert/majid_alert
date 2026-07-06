from datetime import datetime


def percent_change(old_price: float, new_price: float) -> float:
    if old_price == 0:
        return 0
    return ((new_price - old_price) / old_price) * 100


def format_number(value):
    try:
        value = float(value)

        if value >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"

        if value >= 1_000_000:
            return f"{value/1_000_000:.2f}M"

        if value >= 1_000:
            return f"{value/1_000:.2f}K"

        return f"{value:.2f}"

    except:
        return str(value)


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def make_message(title, symbol, price, change, volume, score):

    return (
        f"{title}\n\n"
        f"🪙 {symbol}\n"
        f"💲 Price : {price}\n"
        f"📊 Change : {change:.2f}%\n"
        f"📦 Volume : {format_number(volume)}\n"
        f"⭐ Score : {score}/100\n"
        f"🕒 {now()}"
    )