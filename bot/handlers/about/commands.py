from telegram import Update
from telegram.ext import CallbackContext


def about_cmd(update: Update, _context: CallbackContext):
    update.message.reply_markdown_v2(
        "The source code of the bot available via [GitHub repository]"
        "(https://github.com/unaimillan/sublime-telegram-bot)",
        disable_web_page_preview=True)
