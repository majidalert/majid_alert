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


def make_message(
    title,
    symbol,
    price,
    change,
    volume,
    score,
    resistance=None,
    support=None,
    signal=None,
    pump=None,
    dump=None,
    unusual_volume=None,
    **kwargs
):

    msg = (
        f"🚨 MAJID ALERT AI\n\n"
        f"{title}\n\n"
        f"🪙 ارز: {symbol}\n"
        f"💰 قیمت: {price}\n"
        f"📈 تغییر: {change:.2f}%\n"
        f"📦 حجم: {format_number(volume)}\n"
        f"⭐ امتیاز: {score}/100\n"
    )

    if resistance:
        msg += f"🔴 مقاومت: {resistance}\n"

    if support:
        msg += f"🟢 حمایت: {support}\n"

    if signal:
        msg += f"🎯 سیگنال: {signal}\n"

    if pump:
        msg += "🚀 پامپ غیرعادی تشخیص داده شد\n"

    if dump:
        msg += "⚠️ دامپ غیرعادی تشخیص داده شد\n"

    if unusual_volume:
        msg += "📊 حجم غیرعادی تشخیص داده شد\n"

    msg += f"\n🕒 {now()}"

    return msg