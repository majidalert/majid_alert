import asyncio
from scanner import MarketScanner
from telegram_bot import TelegramNotifier
from config import *

scanner = MarketScanner()
telegram = TelegramNotifier(BOT_TOKEN, CHAT_ID)

async def run():

    print("Majid Alert AI Started...")

    while True:

        try:

            alerts = await scanner.scan()

            for alert in alerts:

                await telegram.send(alert)

        except Exception as e:

            print(e)

        await asyncio.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    asyncio.run(run())