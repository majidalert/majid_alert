import asyncio

from scanner import MarketScanner
from telegram_bot import TelegramNotifier
from config import *


scanner = MarketScanner()

telegram = TelegramNotifier(
    BOT_TOKEN,
    CHAT_ID
)



async def run():

    print("=" * 50)
    print("🚨 MAJID ALERT AI PRO STARTED")
    print("=" * 50)



    while True:

        try:

            alerts = await scanner.scan()



            if alerts:

                print(
                    f"{len(alerts)} Alert(s) Found"
                )



                for alert in alerts:

                    try:

                        await telegram.send(
                            alert
                        )


                    except Exception as e:

                        print(
                            "Telegram Error:",
                            e
                        )



            else:

                print(
                    "No Alert"
                )



        except Exception as e:

            print(
                "Scanner Error:",
                e
            )



        await asyncio.sleep(
            SCAN_INTERVAL
        )





async def shutdown():

    await scanner.close()





if __name__ == "__main__":


    try:

        asyncio.run(
            run()
        )


    except KeyboardInterrupt:

        print(
            "Stopped By User"
        )


    finally:

        try:

            asyncio.run(
                shutdown()
            )

        except:

            pass