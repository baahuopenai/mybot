from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, filters,CallbackContext
import logging

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





app = ApplicationBuilder().token("8014975062:AAE5zNoop2OG-osWO2EUpqAX6kUQrA7PFfg").build()

app.add_handler(CommandHandler("hello", hello))

# on non command i.e message - echo the message on Telegram

#app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))



app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

app.run_polling()
