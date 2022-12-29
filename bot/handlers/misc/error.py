import logging

from telegram import Update
from telegram.ext import CallbackContext


def bot_error_handler(update: Update, context: CallbackContext) -> None:
    logging.error("Exception while handling an update:", exc_info=context.error)
    update.effective_chat.send_message('An error occurred while processing the update.')
