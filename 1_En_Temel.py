import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

class Bot:
    def __init__(self):
        self.application = Application.builder().token(self.get_bot_token()).build()
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_update_recieved)
        )

    def get_bot_username(self):
        return "ReqPullBot"

    def get_bot_token(self):
        return os.getenv("BOT_TOKEN", "")

    async def on_update_recieved(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update)

    def run(self):
        self.application.run_polling()
