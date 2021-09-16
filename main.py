import logging
import os.path
from os import getenv

import telegram.ext
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

from bot.commands import hello_cmd, echo_cmd, pin_message_cmd, slap_cmd, me_cmd, \
    unknown_command_cmd, shrug_cmd, google_cmd, get_cmd, list_cmd, set_cmd, \
    del_cmd, credits_cmd, pidor_cmd, pidoreg_cmd

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s \
                    - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Load configs and create bot instance
load_dotenv()  # load telegram bot token from .env file
API_TOKEN = getenv("TELEGRAM_BOT_API_SECRET", "")
logger.debug("Beginning of token: %s", API_TOKEN[:5])
if not os.path.exists('storage'):
    os.mkdir('storage')
updater = Updater(API_TOKEN, use_context=True,
                  persistence=telegram.ext.PicklePersistence(
                      filename='storage/data.bin'))
dispatch = updater.dispatcher
not_edited = ~Filters.update.edited_message

# Setup dispatcher with callbacks
dispatch.add_handler(CommandHandler('hello', hello_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('slap', slap_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('me', me_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('shrug', shrug_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('google', google_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('pin', pin_message_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('credits', credits_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('get', get_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('list', list_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('set', set_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('del', del_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('pidor', pidor_cmd, filters=not_edited))
dispatch.add_handler(CommandHandler('pidoreg', pidoreg_cmd, filters=not_edited))
updater.dispatcher.add_handler(
    MessageHandler(Filters.regex(r'^/\w+') & not_edited, unknown_command_cmd))
updater.dispatcher.add_handler(
    MessageHandler(Filters.text & ~Filters.update.edited_message, echo_cmd))

# Run the bot
updater.start_polling()
updater.idle()
