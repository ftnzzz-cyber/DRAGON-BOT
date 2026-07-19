import requests
import sqlite3
import logging
from urllib.parse import quote
import time
from telegram import Update, ChatPermissions
from telegram.constants import ChatMemberStatus
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
db = sqlite3.connect("dragon.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    user_id INTEGER PRIMARY KEY,
    warns INTEGER DEFAULT 0
)
""")

db.commit()

# ================= ADMIN CHECK =================

async def is_admin(update, context, user_id):

    member = await context.bot.get_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user_id
    )

    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    )


# ================= WARNING DATABASE =================

def get_warns(user_id):

    cursor.execute(
        "SELECT warns FROM warnings WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return 0


def add_warn(user_id):

    warns = get_warns(user_id) + 1

    cursor.execute(
        """
        INSERT OR REPLACE INTO warnings
        (user_id, warns)
        VALUES (?, ?)
        """,
        (user_id, warns)
    )

    db.commit()

    return warns


def reset_warn(user_id):

    cursor.execute(
        "DELETE FROM warnings WHERE user_id=?",
        (user_id,)
    )

    db.commit()

TOKEN = "8851456984:AAHON0_Aifp3aUnCtIHDoHfgXbK4Yt-uQCI"
OMDB_KEY = "6a386ee3"
OPENROUTER_API_KEY = "sk-or-vl-lcc...af0"

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

warnings = {}

# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🐉 DRAGON ASSIST\n\n"
        "🎬 Movie Assistant Online\n\n"
        "Commands:\n"
        "/movie\n"
        "/trailer\n"
        "/alive\n"
        "/help"
        "/ping"
    )

    await update.message.reply_text(text)

# ---------------- HELP ----------------

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "📜 DRAGON COMMANDS\n\n"

        "🎬 /movie <name>\n"

        "▶️ /trailer <name>\n"
        
        "🤖 /ask <question>"
        
        "⚠️ /warn\n"

        "🔇 /mute\n"

        "🚫 /ban\n"

        "🧹 /purge\n"

        "📊 /alive\n"
        
        "📊 /stats\n"

        "📜 /rules\n"

        "🆔 /id"

    )

# ---------------- ALIVE ----------------

async def alive(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🐉 DRAGON ASSIST\n\n"

        "🟢 Status : Online\n"

        "🎬 Movie Engine : Running\n"

        "🛡 Security : Active\n"

        "⚡ Version : 2.0"

    )

# ---------------- RULES ----------------

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "📜 GROUP RULES\n\n"

        "1. No Spam\n"

        "2. No Links\n"

        "3. Respect Everyone\n"

        "4. Enjoy Movies 🍿"

    )

# ---------------- ID ----------------

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        f"🆔 {update.effective_user.id}"

    )

# ---------------- MOVIE ----------------

async def search_movie(update, movie):

    url = f"https://www.omdbapi.com/?apikey={OMDB_KEY}&t={quote(movie)}"

    try:

        r = requests.get(url)

        data = r.json()

        if data["Response"] == "False":

            await update.message.reply_text("❌ Movie Not Found")

            return

        msg = (

            f"🎬 {data['Title']}\n\n"

            f"⭐ {data['imdbRating']}\n"

            f"📅 {data['Year']}\n"

            f"🎭 {data['Genre']}\n"

            f"🎬 {data['Director']}\n\n"

            f"{data['Plot']}"

        )

        if data["Poster"] != "N/A":

            await update.message.reply_photo(

                photo=data["Poster"],

                caption=msg

            )

        else:

            await update.message.reply_text(msg)

    except:

        await update.message.reply_text(

            "⚠️ Movie Server Error"

        )

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(

            "/movie Avatar"

        )

        return

    await search_movie(

        update,

        " ".join(context.args)

    )

# ---------------- TRAILER ----------------

async def trailer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(

            "/trailer Avatar"

        )

        return

    name = " ".join(context.args)

    url = (

        "https://www.youtube.com/results?search_query="

        + quote(name + " official trailer")

    )

    await update.message.reply_text(

        f"▶️ {url}"

    )
    
# ---------------- AI ASK ----------------

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Example:\n/ask What is AI?"
        )
        return

    question = " ".join(context.args)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        answer = result["choices"][0]["message"]["content"]

        await update.message.reply_text(answer)

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "❌ AI server error."
        )
        
        
# ---------------- WELCOME ----------------

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for member in update.message.new_chat_members:

        await update.message.reply_text(

            f"👋 Welcome {member.first_name}\n\n"

            "🍿 Enjoy DRAGON Movie Group"

        )
       
 # ---------------- WARN ---------------
 
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):

    admin = await is_admin(
        update,
        context,
        update.effective_user.id
    )

    if not admin:
        await update.message.reply_text(
            "❌ Admin only."
        )
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to a user."
        )
        return

    user = update.message.reply_to_message.from_user

    warns = add_warn(user.id)

    await update.message.reply_text(
        f"⚠️ {user.first_name}\n"
        f"Warnings: {warns}/3"
    )

    if warns >= 3:
        try:
            await context.bot.ban_chat_member(
                update.effective_chat.id,
                user.id
            )

            reset_warn(user.id)

            await update.message.reply_text(
                f"🚫 {user.first_name} banned!"
            )

        except Exception as e:
            print(e)
# ---------------- MUTE ----------------

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context, update.effective_user.id):
        await update.message.reply_text("❌ Admin only.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a user's message.")
        return

    user = update.message.reply_to_message.from_user

    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False
            )
        )

        await update.message.reply_text(
            f"🔇 {user.first_name} has been muted."
        )

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Failed to mute user.")


# ---------------- BAN ----------------

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context, update.effective_user.id):
        await update.message.reply_text("❌ Admin only.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a user's message.")
        return

    user = update.message.reply_to_message.from_user

    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id
        )

        await update.message.reply_text(
            f"🚫 {user.first_name} has been banned."
        )

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Failed to ban user.")


# ---------------- PURGE ----------------

async def purge(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context, update.effective_user.id):
        await update.message.reply_text("❌ Admin only.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "⚠️ Reply to a message, then use /purge <count>"
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Example: /purge 10"
        )
        return

    try:
        count = int(context.args[0])

        if count < 1 or count > 100:
            await update.message.reply_text(
                "Choose a number between 1 and 100."
            )
            return

        start_id = update.message.reply_to_message.message_id

        for msg_id in range(start_id, start_id + count):
            try:
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=msg_id
                )
            except Exception:
                pass

        await update.message.delete()

    except ValueError:
        await update.message.reply_text(
            "❌ Enter a valid number."
        )

# ---------------- STATS ----------------

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.effective_chat

    members = await context.bot.get_chat_member_count(chat.id)

    await update.message.reply_text(
        f"📊 DRAGON ASSIST STATS\n\n"
        f"👥 Members: {members}\n"
        f"🆔 Group ID: {chat.id}\n"
        f"📝 Group Name: {chat.title}"
    )
    
 # ---------------- PING ----------------

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):

    start = time.perf_counter()

    msg = await update.message.reply_text("🏓 Pinging...")

    end = time.perf_counter()

    ms = (end - start) * 1000

    await msg.edit_text(
        f"🏓 Pong!\n\n⚡ {ms:.0f} ms"
    )
    
    
#---------------- AUTO MOVIE SEARCH ----------------

async def auto_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    # Ignore commands
    if text.startswith("/"):
        return

    # Ignore links
    if (
        "http://" in text.lower()
        or "https://" in text.lower()
        or "t.me/" in text.lower()
    ):
        return

    # Search movie automatically
    await search_movie(update, text)


# ---------------- ANTI LINK ----------------

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    text = update.message.text.lower()

    if (
        "http://" in text
        or
        "https://" in text
        or
        "t.me/" in text
    ):

        try:

            await update.message.delete()

            await context.bot.send_message(
                update.effective_chat.id,
                "🚫 Links are not allowed!"
            )

        except Exception as e:
            print(e)


# ---------------- BOT ----------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("alive", alive))
app.add_handler(CommandHandler("movie", movie))
app.add_handler(CommandHandler("trailer", trailer))
app.add_handler(CommandHandler("ask", ask))
app.add_handler(CommandHandler("id", user_id))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("purge", purge))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("ping", ping))

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

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        auto_movie
    )
)

print("🐉 DRAGON ASSIST V3 RUNNING...")

app.run_polling()