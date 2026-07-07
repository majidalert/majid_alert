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

    async def get_markets(self):
        session = await self.get_session()

        url = (
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=volume_desc&per_page=250&page=1&sparkline=false"
        )

        async with session.get(url) as response:
            data = await response.json()
            return data

    async def scan(self):
        alerts = []

        try:
            coins = await self.get_markets()

            for coin in coins:
                try:
                    symbol = coin["symbol"].upper() + "USDT"
                    price = float(coin["current_price"])
                    change = float(coin.get("price_change_percentage_24h") or 0)
                    volume = float(coin.get("total_volume") or 0)
                    high = float(coin.get("high_24h") or price)

                    score = 0

                    if change >= PUMP_PERCENT:
                        score += 40

                    if change <= DUMP_PERCENT:
                        score += 40

                    distance = ((high - price) / high) * 100 if high else 0

                    if (
                        distance <= NEAR_HIGH_PERCENT
                        and self.state.can_send(symbol, "HIGH")
                    ):
                        alerts.append(
                            make_message(
                                "🔥 نزدیک سقف ۲۴ ساعته",
                                symbol,
                                price,
                                change,
                                volume,
                                score + 20,
                            )
                        )

                    if (
                        change >= PUMP_PERCENT
                        and self.state.can_send(symbol, "PUMP")
                    ):
                        alerts.append(
                            make_message(
                                "🚀 پامپ",
                                symbol,
                                price,
                                change,
                                volume,
                                score,
                            )
                        )

                    if (
                        change <= DUMP_PERCENT
                        and self.state.can_send(symbol, "DUMP")
                    ):
                        alerts.append(
                            make_message(
                                "📉 دامپ",
                                symbol,
                                price,
                                change,
                                volume,
                                score,
                            )
                        )

                except Exception as e:
                    print(e)

                await asyncio.sleep(0.05)

        except Exception as e:
            print("Scanner:", e)

        return alerts

    async def close(self):
        if self.session:
            await self.session.close()