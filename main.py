import logging
from os import getenv

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler
from telegram.ext.filters import Filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s \
                    - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hello(update: Update, _context: CallbackContext):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def echo(update: Update, _context: CallbackContext):
    update.message.delete()
    update.message.reply_text(update.message.text)


def pin_message(update: Update, _context: CallbackContext):
    update.message.reply_to_message.pin()


load_dotenv()  # load telegram bot token from .env file
API_TOKEN = getenv("TELEGRAM_BOT_API_SECRET", "")
logger.debug("Beginning of token: %s", API_TOKEN[:5])
updater = Updater(API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('hello', hello))
dispatcher.add_handler(MessageHandler(Filters.regex(r'^pin$'), pin_message))
dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
updater.idle()
