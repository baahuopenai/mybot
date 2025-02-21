from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, filters,CallbackContext
import logging
import instaloader
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#    """Echo the user message."""
#   await update.message.reply_text(update.message.text)


# on non command i.e message - echo the message on Telegram
async def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Welcome, {member.first_name}! by keshava🎉 Radhe Radhe  @Fitoortera")


async def get_all_photos(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide an Instagram username!")
        return

    username = context.args[0]
    try:
        # Download Instagram profile's media
        update.message.reply_text(f"Downloading all posts from {username}...")

        # Download posts
        profile = instaloader.Profile.from_username(L.context, username)
        for post in profile.get_posts():
            L.download_post(post, target=username)

            # Find downloaded image
            for file in os.listdir(username):
                if file.endswith(".jpg") or file.endswith(".png"):
                    file_path = os.path.join(username, file)
                    with open(file_path, "rb") as photo:
                        update.message.reply_photo(photo)
                    os.remove(file_path)  # Delete after sending

        update.message.reply_text("✅ All posts have been sent!")

    except Exception as e:
        update.message.reply_text(f"❌ Error fetching posts: {e}")


app = ApplicationBuilder().token("8014975062:AAE5zNoop2OG-osWO2EUpqAX6kUQrA7PFfg").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("allphotos", get_all_photos))

# on non command i.e message - echo the message on Telegram

#app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))



app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

app.run_polling()
