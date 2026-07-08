from telegram import Bot
from telegram.constants import ParseMode


class TelegramNotifier:

    def __init__(self, token, chat_id):

        self.bot = Bot(token=token)

        self.chat_id = chat_id

    async def send(self, message):

        if not message:
            return False

        try:

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )

            print("✅ Alert Sent")

            return True

        except Exception as e:

            print("Telegram Error:", e)

            return False

    async def send_error(self, error):

        try:

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"⚠️ <b>Robot Error</b>\n\n<code>{error}</code>",
                parse_mode=ParseMode.HTML,
            )

        except Exception:

            pass

    async def send_start_message(self):

        try:

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=(
                    "🤖 <b>MAJID ALERT AI PRO</b>\n\n"
                    "✅ ربات با موفقیت اجرا شد."
                ),
                parse_mode=ParseMode.HTML,
            )

        except Exception:

            pass