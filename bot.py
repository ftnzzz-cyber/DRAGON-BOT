import requests
from urllib.parse import quote

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


TOKEN = "8851456984:AAHON0_Aifp3aUnCtIHDoHfgXbK4Yt-uQCI"
OMDB_KEY = "6a386ee3"


# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐉 DRAGON ASSIST MOVIE BOT\n\n"
        "🎬 Your movie companion is online!\n\n"
        "Use /help to see commands 🍿"
    )


# ================= MOVIE SEARCH =================

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "🎬 Example:\n/movie scarface"
        )
        return

    name = " ".join(context.args)

    url = (
        f"https://www.omdbapi.com/"
        f"?apikey={OMDB_KEY}&t={name}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("Response") != "True":
            await update.message.reply_text(
                "❌ Movie not found!"
            )
            return


        info = (
            f"🎬 {data.get('Title')}\n\n"
            f"⭐ Rating: {data.get('imdbRating')}\n"
            f"📅 Year: {data.get('Year')}\n"
            f"🎭 Genre: {data.get('Genre')}\n"
            f"🎬 Director: {data.get('Director')}\n"
            f"👥 Actors: {data.get('Actors')}\n\n"
            f"📝 {data.get('Plot')}"
        )


        poster = data.get("Poster")

        if poster and poster != "N/A":
            await update.message.reply_photo(
                photo=poster,
                caption=info
            )
        else:
            await update.message.reply_text(info)


    except Exception as e:
        print(e)
        await update.message.reply_text(
            "⚠️ Movie server error!"
        )


# ================= TRAILER =================

async def trailer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "▶️ Example:\n/trailer Avatar"
        )
        return


    movie = " ".join(context.args)

    search = quote(
        movie + " official trailer"
    )

    link = (
        "https://www.youtube.com/results?"
        f"search_query={search}"
    )


    await update.message.reply_text(
        f"🎬 {movie} Trailer\n\n"
        f"▶️ Watch:\n{link}"
    )


# ================= STATUS =================

async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🐉 DRAGON ASSIST v2.0\n\n"
        "🟢 Bot: Online\n"
        "🎬 Movie Engine: Active\n"
        "▶️ Trailer Engine: Active\n"
        "🛡 Security: Active\n"
        "⚡ System: Stable"
    )


# ================= USER ID =================

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        f"🆔 Your ID:\n{update.effective_user.id}"
    )


# ================= RULES =================

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📜 GROUP RULES\n\n"
        "1️⃣ No spam\n"
        "2️⃣ No unwanted links\n"
        "3️⃣ Respect members\n"
        "4️⃣ Enjoy movies 🍿"
    )


# ================= HELP =================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🐉 DRAGON ASSIST COMMANDS\n\n"
        "🎬 /movie <name>\n"
        "▶️ /trailer <name>\n"
        "📊 /alive\n"
        "🆔 /id\n"
        "📜 /rules\n"
        "❓ /help\n\n"
        "🛡 Anti-link enabled"
    )


# ================= WELCOME =================

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for member in update.message.new_chat_members:

        await update.message.reply_text(
            f"👋 Welcome {member.first_name}!\n"
            "🍿 Enjoy DRAGON Movie Group"
        )


# ================= ANTI LINK =================

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message and update.message.text:

        text = update.message.text.lower()

        if (
            "http://" in text
            or "https://" in text
            or "t.me/" in text
        ):

            try:
                await update.message.delete()

                await update.message.reply_text(
                    "🚫 Links are not allowed!"
                )

            except Exception as e:
                print(e)



# ================= BOT SETUP =================

app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movie", movie))
app.add_handler(CommandHandler("trailer", trailer))
app.add_handler(CommandHandler("alive", alive))
app.add_handler(CommandHandler("id", user_id))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("help", help_command))


app.add_handler(
    MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome
    )
)


app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        anti_link
    )
)


print("🐉 DRAGON ASSIST v2.0 RUNNING...")
app.run_polling()