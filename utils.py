from datetime import datetime


def format_number(value):

    try:

        value = float(value)

        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"

        if value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"

        if value >= 1_000:
            return f"{value / 1_000:.2f}K"

        if value >= 1:
            return f"{value:.4f}"

        return f"{value:.8f}"

    except:

        return str(value)


def format_percent(value):

    try:
        return f"{float(value):.2f}%"

    except:
        return "-"


def now():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def score_level(score):

    if score >= 95:
        return "🔥 بسیار عالی"

    if score >= 90:
        return "🔴 بسیار قوی"

    if score >= 80:
        return "🟠 قوی"

    if score >= 60:
        return "🟡 متوسط"

    return "🟢 ضعیف"


def make_message(
    title,
    symbol,
    price,
    change,
    volume,
    score,
    resistance=None,
    support=None,
    psychological=None,
    mss_reason=None,
    extension=None,
    multitrade_score=None,
    tp1=None,
    tp2=None,
    tp3=None,
    correction_probability=None,
    breakout_probability=None,
    entry_status=None,
):

    message = (

        "🚨 MAJID ALERT AI PRO\n\n"

        f"{title}\n\n"

        f"SYMBOL={symbol}\n"

        f"🪙 ارز : {symbol}\n"

        f"💰 قیمت : {format_number(price)}\n"

        f"📈 تغییر : {format_percent(change)}\n"

        f"📦 حجم : {format_number(volume)}\n"

    )

    if extension is not None:

        message += (
            f"\n📈 رشد از کف : "
            f"{format_percent(extension)}\n"
        )

    if resistance:

        if isinstance(resistance, dict):

            message += "\n🟥 مقاومت‌های مهم\n"

            for tf, value in resistance.items():

                message += (
                    f"🔸 {tf} : "
                    f"{format_number(value)}\n"
                )

        else:

            message += (
                f"\n🟥 مقاومت : "
                f"{format_number(resistance)}\n"
            )

    if support:

        message += (
            f"\n🟩 حمایت : "
            f"{format_number(support)}\n"
        )

    if psychological:

        message += (
            f"\n🎯 عدد روانی : "
            f"{format_number(psychological)}\n"
        )

    if entry_status:

        message += (
            f"\n🎯 وضعیت مولتی‌ترید : "
            f"{entry_status}\n"
        )

    if tp1:

        message += (
            f"\n🎯 TP1 : "
            f"{format_number(tp1)}"
        )

    if tp2:

        message += (
            f"\n🎯 TP2 : "
            f"{format_number(tp2)}"
        )

    if tp3:

        message += (
            f"\n🎯 TP3 : "
            f"{format_number(tp3)}\n"
        )

    if correction_probability is not None:

        message += (
            f"\n📉 احتمال اصلاح : "
            f"{correction_probability:.0f}%"
        )

    if breakout_probability is not None:

        message += (
            f"\n🚀 احتمال شکست مقاومت : "
            f"{breakout_probability:.0f}%"
        )

    if "پامپ" in title:

        message += (
            "\n🚀 احتمال ادامه روند صعودی وجود دارد.\n"
        )

    if "دامپ" in title:

        message += (
            "\n📉 احتمال ادامه فشار فروش وجود دارد.\n"
        )

    if "هیجان" in title:

        message += (
            "\n🔥 ورود هیجانی معامله‌گران مشاهده شده است.\n"
        )

    if "حرکت غیرعادی" in title:

        message += (
            "\n⚡ نوسان غیرعادی در بازار شناسایی شد.\n"
        )

    if "حجم غیرعادی" in title:

        message += (
            "\n📦 حجم معاملات به شکل غیرمعمول افزایش یافته است.\n"
        )

    if mss_reason:

        message += (
            "\n📌 دلایل سیگنال:\n"
            f"{mss_reason}\n"
        )

    message += (
        f"\n⭐ MSS Score : {score}/100\n"
    )

    if multitrade_score is not None:

        message += (
            f"🎯 MultiTrade Score : "
            f"{multitrade_score}/100\n"
        )

    message += (

        f"🏆 کیفیت سیگنال : "
        f"{score_level(score)}\n"

        f"🕒 {now()}"

    )

    return message