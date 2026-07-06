import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن مستقیم در کد
TOKEN = "8933933120:AAGO1Bn_zy_gWw3BriWdlajr5Er4Ks-0y0A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 ربات پرنسسی فعال شد! 🚀\n\n"
        "✨ من یک ربات تولید محتوای پرنسسی هستم.\n"
        "📢 برای مشاهده محتواها به کانال @princessnature9 بپیوندید."
    )

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🚀 ربات پرنسسی روشن شد...")
    print("📢 برای تست، به ربات پیام /start بفرستید")

    app.run_polling()

if __name__ == "__main__":
    main()
