import os  # noqa: I001
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

load_dotenv()

class Bot:
    def __init__(self):
        
        next_button = InlineKeyboardButton(text="İleri", callback_data="ileri")
        back_button = InlineKeyboardButton(text="Geri", callback_data="geri")
        
        url_button = InlineKeyboardButton(
            text="NetworkRose",
            url="https://networkrose.is-a.dev/"
        )
        
        self.keyboard_m1 = InlineKeyboardMarkup([[next_button]])
        self.keyboard_m2 = InlineKeyboardMarkup([[back_button], [url_button]])

        self.application = (
            Application.builder()
            .token(self.get_bot_token())
            .post_init(self.post_init)
            .build()
        )
        
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CallbackQueryHandler(self.button_tap))

        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_update_received)
        )

    def get_bot_token(self):
        return os.getenv("BOT_TOKEN", "")

    async def send_text(self, who, what):
        ...

    async def copy_message(self, who, msg_id):
        ...

    async def post_init(self, application):
        ...
    
    async def send_menu(self, who, txt, kb):
        try:
            await self.application.bot.send_message(
                chat_id=who,
                text=txt,
                reply_markup=kb,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"Menü gönderilemedi. Hata: {e}")

    async def button_tap(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data
        
        if data == "ileri":
            await query.edit_message_text(text="<i>Menu 2</i>", parse_mode="HTML")
            await query.edit_message_reply_markup(reply_markup=self.keyboard_m2)
        elif data == "geri":
            await query.edit_message_text(text="<i>Menu 1</i>", parse_mode="HTML")
            await query.edit_message_reply_markup(reply_markup=self.keyboard_m1)
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_message.from_user.id
        await self.send_menu(
            user_id,
            "<i>Menu 1</i>",
            self.keyboard_m1
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ...

    async def upper_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ...

    async def lower_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ...

    async def on_update_received(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ...

    def run(self):
        self.application.run_polling()
