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

            return [
                coin["symbol"]
                for coin in result
                if coin.get("quoteCoin") == "USDT"
            ]



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



        if avg_volume > 0:

            if volume >= avg_volume * VOLUME_MULTIPLIER:
                score += 10


        return (
            score,
            high3,
            high7,
            avg_volume
        )



    async def scan(self):

        alerts = []

        symbols = await self.get_symbols()


        for symbol in symbols:

            try:

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



                if change < MIN_RISE_FROM_LOW:
                    continue



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



                daily_distance = (
                    (high24 - price)
                    /
                    high24
                ) * 100



                if daily_distance <= DAILY_RESISTANCE_DISTANCE:
                    score += 15



                if change >= PUMP_PERCENT:
                    score += 10



                pump_scalp = False

                if (
                    change >= 50
                    and avg_volume > 0
                    and volume >= avg_volume * 3
                ):

                    pump_scalp = True



                short_signal = False


                if (
                    change >= 80
                    and daily_distance <= DAILY_RESISTANCE_DISTANCE
                    and avg_volume > 0
                    and volume >= avg_volume * 3
                ):

                    short_signal = True
                    score += 20



                psychological = False

                round_price = round(price)

                if price > 0:

                    if abs(price - round_price) / price < 0.005:

                        psychological = True
                        score += 5



                mss_score = 0


                if change >= 50:

                    mss_score += 5


                if avg_volume > 0 and volume >= avg_volume * 2:

                    mss_score += 5


                score += mss_score

                score = min(score, 100)



                if score < MIN_SCORE:
                    continue



                if short_signal and pump_scalp:

                    title = "⚠️ پامپ قوی + بررسی SHORT"

                elif short_signal:

                    title = "🟥 بررسی موقعیت SHORT"


                elif pump_scalp:

                    title = "🔥 پامپ قوی - اسکالپ"


                elif high7:

                    distance_week = (
                        (high7 - price)
                        /
                        high7
                    ) * 100


                    if distance_week <= WEEKLY_RESISTANCE_DISTANCE:

                        title = "🟥 مقاومت هفتگی"

                    else:

                        title = "🚀 پامپ"


                elif high3:

                    distance_three = (
                        (high3 - price)
                        /
                        high3
                    ) * 100


                    if distance_three <= THREE_DAY_RESISTANCE_DISTANCE:

                        title = "🟧 مقاومت ۳ روزه"

                    else:

                        title = "🚀 پامپ"


                elif daily_distance <= DAILY_RESISTANCE_DISTANCE:

                    title = "🟨 مقاومت روزانه"


                else:

                    title = "🚀 پامپ"



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