import logging
import os.path
from os import getenv

import telegram.ext
from dotenv import load_dotenv
from telegram.ext import Updater

from bot.dispatcher import init_dispatcher

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s \
                    - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load configs and create bot instance
load_dotenv()  # load telegram bot token from .env file
API_TOKEN = getenv("TELEGRAM_BOT_API_SECRET", "")
if not os.path.exists('storage'):
    os.mkdir('storage')

updater = Updater(API_TOKEN, persistence=telegram.ext.PicklePersistence(
    filename='storage/data.bin'))
dispatch = updater.dispatcher

# Setup dispatcher
init_dispatcher(updater.dispatcher)

# Run the bot
updater.start_polling()
logger.info(f"https://t.me/{updater.bot.get_me()['username']} started")
updater.idle()
