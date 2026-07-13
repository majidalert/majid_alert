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
            BASE_URL +
            "/v5/market/instruments-info?category=linear"
        ) as response:

            data = await response.json(content_type=None)

            result = (
                data.get("result", {})
                .get("list", [])
            )

            return [
                c["symbol"]
                for c in result
                if c.get("quoteCoin") == "USDT"
            ]


    async def get_ticker(
        self,
        symbol
    ):

        session = await self.get_session()

        async with session.get(
            BASE_URL +
            f"/v5/market/tickers?category=linear&symbol={symbol}"
        ) as response:

            data = await response.json(content_type=None)

            result = (
                data.get("result", {})
                .get("list", [])
            )

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
            f"category=linear"
            f"&symbol={symbol}"
            f"&interval={interval}"
            f"&limit={limit}"
        )

        async with session.get(url) as response:

            data = await response.json(content_type=None)

            return (
                data.get("result", {})
                .get("list", [])
            )


    async def get_high(
        self,
        symbol,
        interval
    ):

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


    async def get_low(
        self,
        symbol,
        interval
    ):

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


    async def weekly_trend(
        self,
        symbol
    ):

        candles = await self.get_candles(
            symbol,
            "W",
            200
        )

        if not candles:
            return None

        return max(
            float(c[2])
            for c in candles
        )


    async def ath_check(
        self,
        symbol,
        price
    ):

        ath = await self.get_weekly_ath(
            symbol
        )

        if not ath:
            return None, 0

        position = (price / ath) * 100

        return ath, round(position, 2)


    async def weekly_growth(
        self,
        symbol,
        price
    ):

        weekly_low = await self.get_low(
            symbol,
            "W"
        )

        if not weekly_low:
            return 0

        return round(
            ((price - weekly_low) / weekly_low) * 100,
            2
        )


    async def get_weekly_ath(
        self,
        symbol
    ):

        candles = await self.get_candles(
            symbol,
            "W",
            200
        )

        if not candles:
            return None

        return max(
            float(c[2])
            for c in candles
        )
        
    async def weekly_trend(
        self,
        symbol
    ):

        candles = await self.get_candles(
            symbol,
            "W",
            6
        )

        if len(candles) < 4:
            return False

        candles = list(reversed(candles))

        highs = [float(c[2]) for c in candles]
        lows = [float(c[3]) for c in candles]

        return (
            highs[-1] > highs[-2]
            and highs[-2] > highs[-3]
            and lows[-1] > lows[-2]
        )

    async def get_average_volume(
        self,
        symbol
    ):

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


    async def volume_check(
        self,
        symbol,
        volume
    ):

        avg = await self.get_average_volume(
            symbol
        )

        if avg <= 0:
            return False

        return volume >= avg * VOLUME_MULTIPLIER


    async def resistance_levels(
        self,
        symbol,
        price
    ):

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

                diff = (
                    abs(
                        item["price"] -
                        r["price"]
                    )
                    /
                    r["price"]
                ) * 100


                if diff < 1:

                    r["name"] += "/" + item["name"]

                    found = True

                    break


            if not found:

                merged.append(item)


        return merged[:3]



    async def near_resistance(
        self,
        price,
        resistance
    ):

        if resistance <= price:
            return False


        distance = (
            (resistance - price)
            /
            price
        ) * 100


        return distance <= FOUR_HOUR_RESISTANCE_DISTANCE



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
        volume_ok
    ):

        score = 0


        if price >= resistance * 0.98:
            score += 40


        if volume_ok:
            score += 35


        if price >= resistance:
            score += 25


        return min(
            score,
            100
        )



    async def correction_probability(
        self,
        stretch,
        near_resistance,
        ath_position
    ):

        score = 0


        if stretch >= 70:
            score += 30


        if near_resistance:
            score += 30


        if ath_position >= 80:
            score += 40


        return min(
            score,
            100
        )
    async def multittrade_score(
        self,
        stretch,
        correction,
        breakout,
        volume_ok,
        ath_position,
        weekly_growth
    ):

        score = 0


        if stretch >= 70:
            score += 20


        if correction >= 70:
            score += 20


        if breakout <= 40:
            score += 15


        if volume_ok:
            score += 15


        if ath_position >= 80:
            score += 15


        if weekly_growth >= 40:
            score += 15


        return min(
            score,
            100
        )



    async def mss_score(
        self,
        stretch,
        correction,
        breakout,
        ath_position,
        weekly_growth
    ):

        score = 0


        if stretch >= 70:
            score += 25


        if correction >= 70:
            score += 25


        if breakout <= 40:
            score += 15


        if ath_position >= 80:
            score += 20


        if weekly_growth >= 40:
            score += 15


        return min(
            score,
            100
        )



    async def calculate_tp(
        self,
        price
    ):

        return {

            "TP1": round(
                price * 0.97,
                6
            ),

            "TP2": round(
                price * 0.94,
                6
            ),

            "TP3": round(
                price * 0.90,
                6
            )

        }



    async def scan(self):

        alerts = []

        symbols = await self.get_symbols()


        for symbol in symbols:

            try:

                # اصلاح خطای mss
                mss_bonus = 0


                ticker = await self.get_ticker(
                    symbol
                )


                if not ticker:
                    continue


                price = float(
                    ticker.get("lastPrice")
                )


                volume = float(
                    ticker.get("turnover24h")
                )


                low24 = float(
                    ticker.get("lowPrice24h")
                )


                if low24 <= 0:
                    continue


                rise = (
                    (price - low24)
                    /
                    low24
                ) * 100



                trend = await self.weekly_trend(
                    symbol
                )


                if trend:
                    mss_bonus += 10



                ath, ath_position = await self.ath_check(
                    symbol,
                    price
                )


                if not ath:
                    continue



                weekly_growth = await self.weekly_growth(
                    symbol,
                    price
                )



                if weekly_growth >= 40:

                    mss_bonus += 15

                elif weekly_growth >= 20:

                    mss_bonus += 10

                elif weekly_growth >= 10:

                    mss_bonus += 5



                if ath_position >= 90:

                    mss_bonus += 20

                elif ath_position >= 75:

                    mss_bonus += 15

                elif ath_position >= 60:

                    mss_bonus += 10



                resistance = await self.resistance_levels(
                    symbol,
                    price
                )


                if not resistance:
                     print(symbol, "رد شد: resistance")
                     continue


                r1 = resistance[0]["price"]



                near = await self.near_resistance(
                    price,
                    r1
                )


                if not near:
                     print(symbol, "رد شد: near")
                     continue
                    
                    
                stretch = await self.stretch_check(
                    symbol,
                    price,
                    r1
                )


                volume_ok = await self.volume_check(
                    symbol,
                    volume
                )


                correction = await self.correction_probability(
                    stretch,
                    near,
                    ath_position
                )


                breakout = await self.breakout_probability(
                    price,
                    r1,
                    volume_ok
                )


                multi_score = await self.multittrade_score(
                    stretch,
                    correction,
                    breakout,
                    volume_ok,
                    ath_position,
                    weekly_growth
                )


                mss = await self.mss_score(
                    stretch,
                    correction,
                    breakout,
                    ath_position,
                    weekly_growth
                )


                # امتیاز نهایی با بونس‌ها
                final_score = min(
                    ((multi_score + mss) / 2)
                    + mss_bonus,
                    100
                )


                if final_score < MIN_SCORE:
                     print(
                         symbol,
                         "Score=",
                         final_score,
                         "Stretch=",
                         stretch,
                         "Weekly=",
                         weekly_growth,
                         "ATH=",
                         ath_position,
                     )
                     continue



                tp = await self.calculate_tp(
                    price
                )



                if self.state.can_send(
                    symbol,
                    "SHORT",
                    price
                ):


                    message = make_message(

                        "🟥 SHORT MULTITRADE SETUP",

                        symbol,

                        price,

                        rise,

                        volume,

                        round(
                            final_score,
                            0
                        ),

                        resistance=resistance,

                        extension=stretch,

                        multitrade_score=multi_score,

                        weekly_growth=weekly_growth,

                        ath=ath,

                        ath_position=ath_position,

                        tp1=tp["TP1"],

                        tp2=tp["TP2"],

                        tp3=tp["TP3"],

                        correction_probability=correction,

                        breakout_probability=breakout,

                        entry_status=
                        "Entry 1 فعال - انتظار مقاومت بعدی"

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