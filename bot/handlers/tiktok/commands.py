import random
import tempfile
from uuid import uuid4

import yt_dlp.utils
from telegram import Update, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import CallbackContext
from yt_dlp import YoutubeDL

from bot.handlers.tiktok.text_static import PROCESSING_STARTED


def get_tt_video(url: str) -> bytes:
    result = b''
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'quiet': True,
            'paths': {
                'home': tmpdir,
            }
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.sanitize_info(ydl.extract_info(url))
            with open(info['requested_downloads'][0]['filepath'], 'rb') as file:
                result = file.read()
    return result


def tt_video_cmd(update: Update, context: CallbackContext) -> None:
    source_url = ''
    if context.args and len(context.args) == 1:
        source_url = context.args[0]
    elif update.effective_message.reply_to_message and len(
            update.effective_message.reply_to_message.text) > 10:
        source_url = update.effective_message.reply_to_message.text
    else:
        update.effective_message.reply_text(
            "Provide a TikTok link after the command or reply to the link")
        return

    try:
        msg = update.effective_message.reply_text(PROCESSING_STARTED)
        update.effective_message.reply_video(get_tt_video(source_url))
        msg.delete()
    except yt_dlp.utils.DownloadError:
        update.effective_chat.send_message(
            'Failed to process the link, please, try another one')


def get_tt_source_url(url: str) -> str:
    ydl_opts = {
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['webpage_url'].replace(info['uploader_id'],
                                           info['uploader'])


def tt_depersonalize_cmd(update: Update, context: CallbackContext) -> None:
    if context.args and len(context.args) == 1:
        source_url = context.args[0]
    elif update.effective_message.reply_to_message and len(
            update.effective_message.reply_to_message.text) > 10:
        source_url = update.effective_message.reply_to_message.text
    else:
        update.effective_message.reply_text(
            "Provide a TikTok link after the command or reply to the link")
        return

    try:
        msg = update.effective_message.reply_text(PROCESSING_STARTED)
        update.effective_chat.send_message(get_tt_source_url(source_url))
        msg.delete()
    except yt_dlp.utils.DownloadError:
        update.effective_chat.send_message(
            'Failed to process the link, please, try another one')


def tt_inline_cmd(update: Update, context: CallbackContext):
    query = update.inline_query.query

    if query == "":
        return

    shuffled = []
    for word in query.split():
        if len(word) > 3:
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
            input_message_content=InputTextMessageContent(' '.join(shuffled))
        )
    ]

    update.inline_query.answer(results)
