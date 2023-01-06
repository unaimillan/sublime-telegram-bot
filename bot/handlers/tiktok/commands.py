import logging
import re
import tempfile
from uuid import uuid4

import yt_dlp.utils
from telegram import Update, InlineQueryResultArticle, \
    InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton, Message, InlineQueryResultCachedVideo
from telegram.ext import CallbackContext
from yt_dlp import YoutubeDL

from bot.handlers.tiktok.text_static import PROCESSING_STARTED


def get_tt_video_info(url: str, download=False) -> str | tuple[str, bytes]:
    result = b''
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'quiet': True,
            'paths': {
                'home': tmpdir,
            }
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.sanitize_info(ydl.extract_info(url, download=download))
            video_link = info['webpage_url'].replace(info['uploader_id'],
                                                     info['uploader'])
            if not download:
                return video_link

            with open(info['requested_downloads'][0]['filepath'], 'rb') as file:
                result = file.read()
    return video_link, result


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
        video_link, video_bytes = get_tt_video_info(source_url, download=True)
        update.effective_message.reply_video(video_bytes,
                                             reply_markup=InlineKeyboardMarkup([
                                                 [
                                                     InlineKeyboardButton(
                                                         text='🔗',
                                                         url=video_link)]]))
        msg.delete()
    except yt_dlp.utils.DownloadError:
        update.effective_chat.send_message(
            'Failed to process the link, please, try another one')


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
        update.effective_chat.send_message(get_tt_video_info(source_url))
        msg.delete()
    except yt_dlp.utils.DownloadError:
        update.effective_chat.send_message(
            'Failed to process the link, please, try another one')


def tt_inline_cmd(update: Update, context: CallbackContext):
    query = update.inline_query.query.strip()

    if not re.match(r'\s*https?://[vmtw.]{0,5}tiktok.com/.*', query):
        return

    if 'tiktok_cache' not in context.bot_data:
        context.bot_data['tiktok_cache'] = {}

    logging.debug(f'Processing inline query: {query}')
    if query not in context.bot_data['tiktok_cache']:
        try:
            video_link, video_bytes = get_tt_video_info(query, download=True)
        except yt_dlp.utils.DownloadError:
            update.inline_query.answer([])
            return

        # Special chat for uploading video to telegram servers
        special_chat_id = -1001856672797
        video_msg: Message = context.bot.send_video(special_chat_id,
                                                    video_bytes, caption=video_link)
        telegram_video_id = video_msg.video.file_id
        context.bot_data['tiktok_cache'][query] = video_link, telegram_video_id
    else:
        video_link, telegram_video_id = context.bot_data['tiktok_cache'][query]

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Link",
            description="Depersonalized link to the TikTok video",
            input_message_content=InputTextMessageContent(video_link),
        ),
        InlineQueryResultCachedVideo(
            id=str(uuid4()),
            video_file_id=telegram_video_id,
            title='Video',
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='🔗', url=video_link)]]),
        ),
    ]

    update.inline_query.answer(results, cache_time=24 * 60 * 60)
