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

        f"🏆 کیفیت سیگنال : {score_level(score)}\n"

        f"🕒 {now()}"

    )

    return message