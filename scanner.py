import aiohttp
import asyncio

from config import *
from utils import make_message
from state import AlertState
from market_history import MarketHistory


class MarketScanner:

    def __init__(self):

        self.state = AlertState(ALERT_COOLDOWN)
        self.history = MarketHistory()
        self.session = None


    async def get_session(self):

        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session


    async def get_symbols(self):

        session = await self.get_session()

        async with session.get(
            BASE_URL +
            "/v5/market/instruments-info?category=linear"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            symbols = [
                coin["symbol"]
                for coin in result
                if coin.get("quoteCoin") == "USDT"
            ]

            print(
                "Total USDT Symbols:",
                len(symbols)
            )

            return symbols


    async def get_ticker(self, symbol):

        session = await self.get_session()

        async with session.get(
            BASE_URL +
            f"/v5/market/tickers?category=linear&symbol={symbol}"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            if not result:
                return None

            return result[0]


    async def calculate_score(self, symbol, price, volume):

        score = 0

        high3, low3 = await self.history.get_three_day_levels(symbol)

        high7, low7 = await self.history.get_week_levels(symbol)

        avg_volume = await self.history.get_average_volume(symbol)


        if low3:

            rise3 = ((price - low3) / low3) * 100

            if rise3 >= MIN_RISE_FROM_LOW:
                score += 25


        if low7:

            rise7 = ((price - low7) / low7) * 100

            if rise7 >= MIN_RISE_FROM_LOW:
                score += 25


        if high3:

            distance = ((high3 - price) / high3) * 100

            if distance <= THREE_DAY_RESISTANCE_DISTANCE:
                score += 20


        if high7:

            distance = ((high7 - price) / high7) * 100

            if distance <= WEEKLY_RESISTANCE_DISTANCE:
                score += 20


        return (
            score,
            high3,
            high7,
            avg_volume
        )


    async def scan(self):

        alerts = []

        symbols = await self.get_symbols()

        checked = 0


        for symbol in symbols:

            try:

                checked += 1

                ticker = await self.get_ticker(symbol)

                if not ticker:
                    continue


                vals = [
                    ticker.get("lastPrice"),
                    ticker.get("highPrice24h"),
                    ticker.get("lowPrice24h"),
                    ticker.get("turnover24h"),
                ]


                if any(v in (None, "") for v in vals):
                    continue


                price = float(vals[0])
                high24 = float(vals[1])
                low24 = float(vals[2])
                volume = float(vals[3])


                if low24 <= 0:
                    continue


                change = (
                    (price - low24)
                    /
                    low24
                ) * 100


                drop = (
                    (high24 - price)
                    /
                    high24
                ) * 100


                (
                    score,
                    high3,
                    high7,
                    avg_volume
                ) = await self.calculate_score(
                    symbol,
                    price,
                    volume
                )
                # ----------------------------
# امتیاز حرکت بازار
# ----------------------------

                if change >= 10:
                    score += 5

                if change >= 20:
                    score += 10

                if change >= 50:
                    score += 15

                if change >= 100:
                    score += 20


                if drop >= 10:
                    score += 5

                if drop >= 20:
                    score += 10

                if drop >= 40:
                    score += 20


                if avg_volume > 0:

                    if volume >= avg_volume * 2:
                        score += 10

                    if volume >= avg_volume * 3:
                        score += 15

                    if volume >= avg_volume * 5:
                        score += 20


                daily_distance = (
                    (high24 - price)
                    /
                    high24
                ) * 100


                if daily_distance <= DAILY_RESISTANCE_DISTANCE:
                    score += 15


                pump_scalp = (

                    change >= 20

                    and

                    avg_volume > 0

                    and

                    volume >= avg_volume * 2

                )


                dump_signal = (

                    drop >= 20

                    and

                    avg_volume > 0

                    and

                    volume >= avg_volume * 2

                )


                short_signal = (

                    change >= 80

                    and

                    daily_distance <= DAILY_RESISTANCE_DISTANCE

                    and

                    avg_volume > 0

                    and

                    volume >= avg_volume * 3

                )


                psychological = False

                round_price = round(price)

                if price > 0:

                    if abs(price - round_price) / price < 0.005:

                        psychological = True
                        score += 5


                score = min(score, 100)


                print(
                    f"SCAN {symbol} | "
                    f"Growth: {change:.2f}% | "
                    f"Drop: {drop:.2f}% | "
                    f"Score: {score}"
                )


                if score < MIN_SCORE:
                    continue
                                    if short_signal and pump_scalp:

                    title = "⚠️ پامپ هیجانی + بررسی SHORT"

                elif short_signal:

                    title = "🟥 بررسی SHORT"

                elif pump_scalp:

                    title = "🚀 پامپ هیجانی"

                elif dump_signal:

                    title = "📉 دامپ هیجانی"

                elif high7:

                    distance_week = (
                        (high7 - price)
                        /
                        high7
                    ) * 100

                    if distance_week <= WEEKLY_RESISTANCE_DISTANCE:

                        title = "🟥 مقاومت هفتگی"

                    else:

                        title = "🚀 حرکت صعودی"

                elif high3:

                    distance_three = (
                        (high3 - price)
                        /
                        high3
                    ) * 100

                    if distance_three <= THREE_DAY_RESISTANCE_DISTANCE:

                        title = "🟧 مقاومت ۳ روزه"

                    else:

                        title = "🚀 حرکت صعودی"

                else:

                    title = "📊 حرکت غیرعادی"


                if psychological:

                    title += " 🔢"


                if not self.state.can_send(symbol, title):

                    print(
                        "Duplicate blocked:",
                        symbol
                    )

                    continue


                message = make_message(
                    title,
                    symbol,
                    price,
                    change,
                    volume,
                    score
                )


                if short_signal:

                    short_sl = high24 * 1.02

                    tp1 = price * 0.95
                    tp2 = price * 0.90
                    tp3 = price * 0.85


                    message += (
                        f"\n\n📉 SHORT PLAN"
                        f"\n🎯 ورود: {price:.8f}"
                        f"\n🛑 حد ضرر: {short_sl:.8f}"
                        f"\n🎯 TP1: {tp1:.8f}"
                        f"\n🎯 TP2: {tp2:.8f}"
                        f"\n🎯 TP3: {tp3:.8f}"
                    )


                if avg_volume > 0:

                    message += (
                        f"\n📊 حجم میانگین: "
                        f"{avg_volume:,.0f}"
                    )


                alerts.append(message)


            except Exception as e:

                print(
                    symbol,
                    e
                )


            await asyncio.sleep(0.05)


        print(
            "Coins Checked:",
            checked,
            "| Alerts:",
            len(alerts)
        )


        return alerts
            async def close(self):

        try:

            if self.session:

                await self.session.close()

        except Exception:

            pass


        try:

            await self.history.close()

        except Exception:

            pass