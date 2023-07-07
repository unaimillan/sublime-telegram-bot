import logging
import os.path
from os import getenv

import sentry_sdk
import telegram.ext
from dotenv import load_dotenv
from sqlmodel import create_engine
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

# sentry_sdk.init(
#     dsn=getenv("SENTRY_DSN", ""),
#     traces_sample_rate=1.0
# )

engine = create_engine(os.getenv("DATABASE_URL", "Error no db url provided"), echo=False)

updater = Updater(API_TOKEN, persistence=telegram.ext.PicklePersistence(
    filename='storage/data.bin'))
dispatch = updater.dispatcher

# Setup dispatcher
init_dispatcher(updater.dispatcher, engine)

# Run the bot
updater.start_polling()
logger.info(f"https://t.me/{updater.bot.get_me()['username']} started")
updater.idle()
