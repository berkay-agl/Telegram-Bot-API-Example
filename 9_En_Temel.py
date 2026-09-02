# Effective message önemi için 8_En_Temel ile karşılaştırın -> mesajın içeriğini değiştirin vs.

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)

load_dotenv()

class Bot:
    def __init__(self):

        self.user_modes = {}

        self.application = (
            Application.builder()
            .token(self.get_bot_token())
            .post_init(self.post_init)
            .build()
        )

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("upper", self.upper_command))
        self.application.add_handler(CommandHandler("lower", self.lower_command))

        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_update_received)
        )

    def get_bot_token(self):
        return os.getenv("BOT_TOKEN", "")

    async def send_text(self, who, what):
        try:
            await self.application.bot.send_message(chat_id=who, text=what)
        except Exception as e:
            print(f"Mesaj gönderilemedi. Hata: {e}")

    async def copy_message(self, who, msg_id):
        ...

    async def post_init(self, application):
        ...

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        chat_id = update.effective_chat.id

        await self.send_text(
            chat_id,
            "Komutlar:\n/upper - /upper değer şeklinde kullanırsan verdiğin değerleri büyük harflerle yazarım.\n"
            "/lower - /lower DEĞER şeklinde kullanırsan verdiğin değerleri küçük harflerle yazarım."
        )

    async def upper_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        chat_id = update.effective_chat.id

        self.user_modes[chat_id] = "upper"

        args = update.effective_message.text.split(" ", 1)
        if len(args) > 1:
            await self.send_text(chat_id, args[1].upper())
        else:
            await self.send_text(chat_id, "Upper modu açıldı.")

    async def lower_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        chat_id = update.effective_chat.id

        self.user_modes[chat_id] = "lower"

        args = update.effective_message.text.split(" ", 1)
        if len(args) > 1:
            await self.send_text(chat_id, args[1].lower())
        else:
            await self.send_text(chat_id, "Lower modu açıldı.")

    async def on_update_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        chat_id = update.effective_chat.id
        text = update.effective_message.text
        mode = self.user_modes.get(chat_id)

        user = update.effective_message.from_user.full_name

        print(f"{user} kullanıcısının modu: {mode}")

        if mode == "upper":
            await self.send_text(chat_id, text.upper())
        elif mode == "lower":
            await self.send_text(chat_id, text.lower())
        else:
            await self.send_text(chat_id, text)

    def run(self):
        self.application.run_polling()
