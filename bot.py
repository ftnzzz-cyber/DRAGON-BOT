from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8851456984:AAEIl9vY72WmYphaAQ1X_7Cs80rXaXWi7Nc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome!\nI'm your Movie Assistant Bot 🤖"
    )
async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 DRAGON Assist is Online!\n\n"
        "🟢 Status: Running\n"
        "🛡️ Protection: Active\n"
        "🎬 Mode: Movie Assistant\n"
        "👑 Owner: FTNEONEZZZ\n\n"
        "Version: 1.0"
    )
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...''
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Welcome {member.first_name}!\nEnjoy the Movie Group! 🍿"
        )

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text.lower()

        if "http://" in text or "https://" in text or "t.me/" in text:
            try:
                await update.message.delete()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="🚫 Links are not allowed in this group!"
                )
            except Exception as e:
                print(e)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("alive", alive))

app.add_handler(
    MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
)
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, anti_link)
)

print("🤖 Bot is running...")
app.run_polling()