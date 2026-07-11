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

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



def format_resistance(resistance):

    if not resistance:
        return ""

    text = "🔴 مقاومت‌ها:\n"


    if isinstance(resistance, list):

        for r in resistance:

            if isinstance(r, dict):

                name = r.get(
                    "name",
                    ""
                )

                price = r.get(
                    "price",
                    ""
                )

                text += (
                    f"   {name} ➜ {price}\n"
                )

            else:

                text += (
                    f"   {r}\n"
                )

    else:

        text += (
            f"   {resistance}\n"
        )


    return text



def format_support(support):

    if not support:
        return ""

    text = "🟢 حمایت‌ها:\n"


    if isinstance(support, list):

        for s in support:

            if isinstance(s, dict):

                name = s.get(
                    "name",
                    ""
                )

                price = s.get(
                    "price",
                    ""
                )

                text += (
                    f"   {name} ➜ {price}\n"
                )

            else:

                text += (
                    f"   {s}\n"
                )

    else:

        text += (
            f"   {support}\n"
        )


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

        f"🚨 MAJID ALERT AI PRO\n\n"

        f"{title}\n\n"

        f"🪙 ارز: {symbol}\n"

        f"💰 قیمت: {price}\n"

        f"📈 تغییر: {change:.2f}%\n"

        f"📦 حجم: {format_number(volume)}\n"

        f"⭐ امتیاز: {score}/100\n"

    )



    if resistance:

        msg += (
            "\n"
            +
            format_resistance(resistance)
        )



    if support:

        msg += (
            "\n"
            +
            format_support(support)
        )



    if kwargs.get("extension"):

        msg += (
            f"\n📈 رشد از کف : "
            f"{kwargs.get('extension')}%\n"
        )



    if kwargs.get("multitrade_score"):

        msg += (
            f"\n🎯 MultiTrade Score: "
            f"{kwargs.get('multitrade_score')}/100\n"
        )



    if kwargs.get("correction_probability"):

        msg += (
            f"📉 احتمال اصلاح : "
            f"{kwargs.get('correction_probability')}%\n"
        )



    if kwargs.get("breakout_probability"):

        msg += (
            f"🚀 احتمال شکست مقاومت : "
            f"{kwargs.get('breakout_probability')}%\n"
        )



    if kwargs.get("tp1"):

        msg += (
            "\n📌 MULTITRADE SHORT\n"

            f"🟥 Entry 1 : {price}\n\n"

            f"🎯 TP1 : {kwargs.get('tp1')}\n"

            f"🎯 TP2 : {kwargs.get('tp2')}\n"

            f"🎯 TP3 : {kwargs.get('tp3')}\n"
        )



    if kwargs.get("ath"):

        msg += (

            "\n🏔 ATH WEEKLY\n"

            f"🔝 سقف تاریخی: "
            f"{format_number(kwargs.get('ath'))}\n"

            f"📊 موقعیت نسبت به ATH: "
            f"{kwargs.get('ath_position')}%\n"

        )



    if signal:

        msg += (
            f"\n🎯 سیگنال: {signal}\n"
        )



    if pump:

        msg += (
            "🚀 پامپ غیرعادی تشخیص داده شد\n"
        )



    if dump:

        msg += (
            "⚠️ دامپ غیرعادی تشخیص داده شد\n"
        )



    if unusual_volume:

        msg += (
            "📊 حجم غیرعادی تشخیص داده شد\n"
        )



    if kwargs.get("entry_status"):

        msg += (
            f"\n📍 {kwargs.get('entry_status')}\n"
        )



    msg += (
        f"\n🕒 {now()}"
    )


    return msg