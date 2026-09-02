import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

class Bot:
    def __init__(self):

        self.application = (
            Application.builder()
            .token(self.get_bot_token())
            .post_init(self.post_init)
            .build()
        )

        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_update_recieved)
        )

    def get_bot_username(self):
        return "ReqPullBot"

    def get_bot_token(self):
        return os.getenv("BOT_TOKEN", "")

    async def on_update_recieved(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ...

    async def send_text(self, who, what):
        try:
            await self.application.bot.send_message(chat_id=who, text=what)
        except Exception as e:
            print(f"{who}'ya mesaj gönderilmedi... hata: {e}")

    async def post_init(self, application):
        await self.send_text(8517915865, "main.py başlatıldı.")

    def run(self):
        self.application.run_polling()
