import random
import re
from urllib.parse import quote as urlquote
from uuid import uuid4

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CallbackContext

from bot.utils import raw_name, escape_markdown2


def hello_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text(
        'Hello, {}!'.format(update.message.from_user.first_name))


def slap_cmd(update: Update, context: CallbackContext):
    update.message.reply_markdown_v2(
        r'\**{}* slaps _{}_ around a bit with a large trout'.format(
            raw_name(update.effective_user),
            escape_markdown2(context.args[0]) if context.args else 'void'))


def me_cmd(update: Update, _context: CallbackContext):
    update.message.reply_markdown_v2(
        r'\**{}* {}'.format(
            raw_name(update.effective_user),
            escape_markdown2(update.message.text[4:])))


def shrug_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text(r'¯\_(ツ)_/¯')


def google_cmd(update: Update, _context: CallbackContext):
    query = update.message.text[8:]
    if not query:
        update.message.reply_text('What should I search for?')
    else:
        update.message.reply_text('https://lmgtfy.com/?q=' +
                                  urlquote(update.message.text[8:]),
                                  disable_web_page_preview=True)


def pin_message_cmd(update: Update, _context: CallbackContext):
    if update.message.reply_to_message:
        update.message.reply_to_message.pin()
    else:
        update.message.reply_markdown_v2('reply to message you want to _pin_')


def echo_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text("{} said {}".format(
        update.effective_user.name,
        update.message.text))


def unknown_command_cmd(update: Update, _context: CallbackContext):
    update.effective_message.reply_text(
        "sorry, this command isn't supported yet(")


def text_inline_cmd(update: Update, context: CallbackContext):
    query = update.inline_query.query

    if query == "":
        return

    shuffled = []
    # Split query by words using regex [a-zA-Z] for all languages
    for word in re.split(r'([^\W\d_]{4,})', query):
        if word.isalnum():
            letters = word[1:-1]
            res = word[0] + ''.join(random.sample(letters, len(letters))) + \
                  word[-1]
            shuffled.append(res)
        else:
            shuffled.append(word)

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Echo",
            description="Just echo what you have typed",
            input_message_content=InputTextMessageContent(query),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            description='Make query text upper case',
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Shuffle',
            description='Shuffle all the letters inside words',
            input_message_content=InputTextMessageContent(''.join(shuffled))
        )
    ]

    update.inline_query.answer(results, cache_time=0)
