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

        self.application.add_handler(
            MessageHandler(filters.PHOTO & ~filters.COMMAND, self.on_update_recieved)
        )

        self.application.add_handler(
            MessageHandler(filters.Document.IMAGE & ~filters.COMMAND, self.on_update_recieved)
        )

    def get_bot_username(self):
        return "ReqPullBot"

    def get_bot_token(self):
        return os.getenv("BOT_TOKEN", "")

    async def on_update_recieved(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        USER_ID = update.message.chat.id

        if update.message:
            text = update.message.text
            await self.send_text(USER_ID, text)

        if update.message.photo:

            photo = update.message.photo[-1].file_id
            file_width = update.message.photo[-1].width
            file_height = update.message.photo[-1].height
            file_size = update.message.photo[-1].file_size

            if file_size < 1024 * 1024:
                kb_size = round(file_size / 1024, 2)
                top_size = f"{kb_size} KB."
            else:
                mb_size = round(file_size / (1024*1024), 2)
                top_size = f"{mb_size} MB."

            await self.send_photo(USER_ID, photo)

            photo_info = (
                f"Resim şu kadar boyutta: {top_size}",
                f"Resim genişlik/yükseklik: {file_width} x {file_height} px",
                "ÖNEMLİ: Bu Telegram'da fotoğrafın sıkıştırılmış değerleridir."
            )

            photo_info_send = "\n".join(photo_info)

            await self.send_text(USER_ID, photo_info_send)

        if update.message.document:

            document_id = update.message.document.file_id
            document_name = update.message.document.file_name
            document_size = update.message.document.file_size

            if document_size < 1024 * 1024:
                kb_size = round(document_size / 1024, 2)
                top_size = f"{kb_size} KB."
            else:
                mb_size = round(document_size / (1024 * 1024), 2)
                top_size = f"{mb_size} MB."

            await self.send_document(USER_ID, document_id)

            photo_info = (
                f"Belge adı: {document_name}",
                f"Belge boyutu: {top_size}",
                "Tamamen orijinal boyutta ele alındı."
            )

            photo_info_send = "\n".join(photo_info)

            await self.send_text(USER_ID, photo_info_send)

    async def send_text(self, who, what):
        try:
            await self.application.bot.send_message(chat_id=who, text=what)
        except Exception as e:
            print(f"{who}'ya mesaj gönderilmedi... hata: {e}")

    async def send_photo(self, who, photo):
        try:
            await self.application.bot.send_photo(chat_id=who, photo=photo)
        except Exception as e:
            print(f"{who}'ya mesaj gönderilmedi... hata: {e}")

    async def send_document(self, who, document):
        await self.application.bot.send_document(chat_id=who, document=document)

    async def post_init(self, application):
        ...

    def run(self):
        self.application.run_polling()
