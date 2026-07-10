import aiohttp
import asyncio

from config import *
from utils import make_message
from state import AlertState


class MarketScanner:

    def __init__(self):

        self.state = AlertState(ALERT_COOLDOWN)
        self.session = None


    async def get_session(self):

        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session


    async def get_symbols(self):

        session = await self.get_session()

        async with session.get(
            BASE_URL + "/v5/market/instruments-info?category=linear"
        ) as response:

            data = await response.json(content_type=None)

            result = data.get("result", {}).get("list", [])

            return [
                c["symbol"]
                for c in result
                if c.get("quoteCoin") == "USDT"
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


    async def get_candles(
        self,
        symbol,
        interval,
        limit=100
    ):

        session = await self.get_session()

        url = (
            BASE_URL +
            f"/v5/market/kline?"
            f"category=linear&symbol={symbol}"
            f"&interval={interval}&limit={limit}"
        )

        async with session.get(url) as response:

            data = await response.json(content_type=None)

            return (
                data.get("result", {})
                .get("list", [])
            )


    async def get_high(self, symbol, interval):

        candles = await self.get_candles(
            symbol,
            interval
        )

        if not candles:
            return None

        return max(
            float(c[2])
            for c in candles
        )


    async def get_low(self, symbol, interval):

        candles = await self.get_candles(
            symbol,
            interval
        )

        if not candles:
            return None

        return min(
            float(c[3])
            for c in candles
        )
    async def get_average_volume(self, symbol):

        candles = await self.get_candles(
            symbol,
            "15",
            50
        )

        if not candles:
            return 0

        volumes = [
            float(c[6])
            for c in candles
        ]

        return sum(volumes) / len(volumes)



    async def volume_check(self, symbol, volume):

        avg = await self.get_average_volume(
            symbol
        )

        if avg <= 0:
            return False

        return volume >= avg * 2



    async def resistance_levels(self, symbol, price):

        raw = []

        levels = [
            ("4H", "240"),
            ("1D", "D"),
            ("3D", "3D"),
            ("1W", "W")
        ]


        for name, interval in levels:

            try:

                high = await self.get_high(
                    symbol,
                    interval
                )

                if high and high > price:

                    raw.append(
                        {
                            "name": name,
                            "price": high
                        }
                    )

            except Exception as e:

                print(
                    "Resistance Error:",
                    symbol,
                    e
                )


        raw.sort(
            key=lambda x: x["price"]
        )


        merged = []


        for item in raw:

            found = False

            for r in merged:

                diff = abs(
                    item["price"] - r["price"]
                ) / r["price"] * 100


                if diff < 1:

                    r["name"] += "/" + item["name"]
                    found = True
                    break


            if not found:

                merged.append(
                    item
                )


        return merged[:3]



    async def stretch_check(
        self,
        symbol,
        price,
        resistance
    ):

        low = await self.get_low(
            symbol,
            "D"
        )

        if not low:
            return 0


        if resistance <= low:
            return 0


        stretch = (
            (price - low)
            /
            (resistance - low)
        ) * 100


        return round(
            stretch,
            2
        )



    async def breakout_probability(
        self,
        price,
        resistance,
        volume
    ):

        score = 0


        if price >= resistance:

            score += 50


        if volume:

            score += 30


        if price > resistance * 1.01:

            score += 20


        return min(
            score,
            100
        )



    async def correction_probability(
        self,
        stretch,
        near_resistance
    ):

        score = 0


        if stretch >= 70:

            score += 50


        if near_resistance:

            score += 30


        if stretch >= 90:

            score += 20


        return min(
            score,
            100
        )



    async def pump_check(
        self,
        price,
        low
    ):

        if low <= 0:
            return False


        change = (
            (price - low)
            /
            low
        ) * 100


        return change >= PUMP_PERCENT



    async def dump_check(
        self,
        price,
        high
    ):

        if high <= 0:
            return False


        drop = (
            (high - price)
            /
            high
        ) * 100


        return drop >= DUMP_PERCENT
    async def multittrade_score(
        self,
        stretch,
        correction,
        breakout,
        volume,
        resistance
    ):

        score = 0


        if stretch >= 70:
            score += 30


        if correction >= 60:
            score += 25


        if breakout < 50:
            score += 20


        if volume:
            score += 15


        if resistance:
            score += 10


        return min(
            score,
            100
        )



    async def mss_score(
        self,
        stretch,
        correction,
        breakout
    ):

        score = 0


        if stretch >= 70:
            score += 40


        if correction >= 60:
            score += 30


        if breakout < 50:
            score += 30


        return min(
            score,
            100
        )



    async def calculate_tp(
        self,
        price
    ):

        return {

            "TP1":
            round(
                price * 0.97,
                6
            ),

            "TP2":
            round(
                price * 0.94,
                6
            ),

            "TP3":
            round(
                price * 0.90,
                6
            )
        }
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


                price = float(
                    ticker.get("lastPrice")
                )

                high = float(
                    ticker.get("highPrice24h")
                )

                low = float(
                    ticker.get("lowPrice24h")
                )

                volume = float(
                    ticker.get("turnover24h")
                )


                if low <= 0:
                    continue


                rise = (
                    (price - low)
                    /
                    low
                ) * 100


                # حذف ارزهای کم حرکت

                if rise < 30:
                    continue



                resistance = await self.resistance_levels(
                    symbol,
                    price
                )


                if not resistance:
                    continue


                r1 = resistance[0]["price"]


                stretch = await self.stretch_check(
                    symbol,
                    price,
                    r1
                )


                correction = await self.correction_probability(
                    stretch,
                    True
                )


                breakout = await self.breakout_probability(
                    price,
                    r1,
                    volume
                )


                volume_ok = await self.volume_check(
                    symbol,
                    volume
                )


                multi_score = await self.multittrade_score(
                    stretch,
                    correction,
                    breakout,
                    volume_ok,
                    True
                )


                mss = await self.mss_score(
                    stretch,
                    correction,
                    breakout
                )


                if multi_score < 70:
                    continue


                if mss < 70:
                    continue
                tp = await self.calculate_tp(
                    price
                )


                if self.state.can_send(
                    symbol,
                    "SHORT"
                ):


                    title = (
                        "🟥 SHORT MULTITRADE SETUP"
                    )


                    resistance_text = ""


                    for r in resistance[:3]:

                        resistance_text += (
                            f"\n🔸 {r['name']} : "
                            f"{r['price']}"
                        )



                    message = make_message(
                        title,
                        symbol,
                        price,
                        rise,
                        volume,
                        multi_score,
                        resistance=resistance
                    )


                    message += (

                        "\n\n📊 SHORT ANALYSIS"

                        f"\n📏 کشیدگی قیمت : {stretch}%"

                        f"\n🔄 احتمال اصلاح : {correction}%"

                        f"\n⚔️ احتمال شکست : {breakout}%"

                        f"\n⭐ MultiTrade Score : {multi_score}/100"

                        f"\n🏆 MSS Score : {mss}/100"


                        "\n\n🎯 TP PLAN"

                        f"\n✅ TP1 : {tp['TP1']}"

                        f"\n✅ TP2 : {tp['TP2']}"

                        f"\n✅ TP3 : {tp['TP3']}"

                        "\n\n📌 MULTITRADE"

                        "\n🟥 Entry 1 : Current"

                        f"\n🟥 Entry 2 : {r1}"

                        "\n🟥 Entry 3 : Next Resistance"


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
