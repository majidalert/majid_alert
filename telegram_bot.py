from telegram import Bot
from telegram.constants import ParseMode


class TelegramNotifier:

    def __init__(self, token, chat_id):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send(self, message):

        try:

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )

            return True

        except Exception as e:

            print("Telegram Error:", e)

            return False