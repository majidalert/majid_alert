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


def format_resistance(resistance):

    if not resistance:
        return ""

    text = "🔴 مقاومت‌ها:\n"

    if isinstance(resistance, list):

        for r in resistance:

            if isinstance(r, dict):
                name = r.get("name", "")
                price = r.get("price", "")

                text += f"   {name} ➜ {price}\n"

            else:
                text += f"   {r}\n"

    else:
        text += f"   {resistance}\n"

    return text


def format_support(support):

    if not support:
        return ""

    text = "🟢 حمایت‌ها:\n"

    if isinstance(support, list):

        for s in support:

            if isinstance(s, dict):
                name = s.get("name", "")
                price = s.get("price", "")

                text += f"   {name} ➜ {price}\n"

            else:
                text += f"   {s}\n"

    else:
        text += f"   {support}\n"

    return text


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
        msg += "\n" + format_resistance(resistance)


    if support:
        msg += "\n" + format_support(support)


    if signal:
        msg += f"\n🎯 سیگنال: {signal}\n"


    if pump:
        msg += "🚀 پامپ غیرعادی تشخیص داده شد\n"


    if dump:
        msg += "⚠️ دامپ غیرعادی تشخیص داده شد\n"


    if unusual_volume:
        msg += "📊 حجم غیرعادی تشخیص داده شد\n"


    msg += f"\n🕒 {now()}"


    return msg