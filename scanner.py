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

            data = await response.json(
                content_type=None
            )

            return [

                coin["symbol"]

                for coin in data.get(
                    "result",
                    {}
                ).get(
                    "list",
                    []
                )

                if coin.get(
                    "quoteCoin"
                ) == "USDT"

            ]



    async def get_ticker(self, symbol):

        session = await self.get_session()

        async with session.get(
            BASE_URL +
            f"/v5/market/tickers?category=linear&symbol={symbol}"
        ) as response:

            data = await response.json(
                content_type=None
            )

            result = data.get(
                "result",
                {}
            ).get(
                "list",
                []
            )


            if not result:

                return None


            return result[0]



    async def calculate_score(
        self,
        symbol,
        last_price,
        volume
    ):

        score = 0

        high3, low3 = await self.history.get_three_day_levels(
            symbol
        )

        high7, low7 = await self.history.get_week_levels(
            symbol
        )

        avg_volume = await self.history.get_average_volume(
            symbol
        )


        if low3:

            rise3 = (
                (last_price - low3)
                /
                low3
            ) * 100


            if rise3 >= MIN_RISE_FROM_LOW:

                score += 25



        if low7:

            rise7 = (
                (last_price - low7)
                /
                low7
            ) * 100


            if rise7 >= MIN_RISE_FROM_LOW:

                score += 25



        if high3:

            distance = (

                (high3 - last_price)
                /
                high3

            ) * 100


            if distance <= THREE_DAY_RESISTANCE_DISTANCE:

                score += 20



        if high7:

            distance = (

                (high7 - last_price)
                /
                high7

            ) * 100


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

                ticker = await self.get_ticker(
                    symbol
                )


                if not ticker:

                    continue



                last_price = float(
                    ticker["lastPrice"]
                )

                high_price = float(
                    ticker["highPrice24h"]
                )

                low_price = float(
                    ticker["lowPrice24h"]
                )

                volume = float(
                    ticker["turnover24h"]
                )



                if low_price <= 0:

                    continue



                change = (

                    (last_price - low_price)
                    /
                    low_price

                ) * 100



                if change < MIN_RISE_FROM_LOW:

                    continue



                score, high3, high7, avg_volume = await self.calculate_score(
                    symbol,
                    last_price,
                    volume
                )



                daily_distance = (

                    (high_price - last_price)
                    /
                    high_price

                ) * 100



                if daily_distance <= DAILY_RESISTANCE_DISTANCE:

                    score += 15



                if change >= PUMP_PERCENT:

                    score += 10



                if score < MIN_SCORE:

                    continue



                if high7:

                    resistance_type = "🟥 مقاومت هفتگی"


                elif high3:

                    resistance_type = "🟧 مقاومت ۳ روزه"


                elif daily_distance <= DAILY_RESISTANCE_DISTANCE:

                    resistance_type = "🟨 مقاومت روزانه"


                else:

                    resistance_type = "🚀 پامپ"



                if not self.state.can_send(
                    symbol,
                    resistance_type
                ):

                    continue



                message = make_message(
                    resistance_type,
                    symbol,
                    last_price,
                    change,
                    volume,
                    score
                )



                if avg_volume > 0:

                    message += (
                        f"\n📊 حجم میانگین: "
                        f"{avg_volume:,.0f}"
                    )



                alerts.append(
                    message
                )



            except Exception as e:

                print(
                    symbol,
                    e
                )



            await asyncio.sleep(
                0.05
            )



        return alerts



    async def close(self):

        if self.session:

            await self.session.close()


        await self.history.close()