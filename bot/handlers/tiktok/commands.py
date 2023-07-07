import logging
import re
import tempfile
from uuid import uuid4

import sentry_sdk
import yt_dlp.utils
from sqlalchemy import or_
from telegram import Update, InlineQueryResultArticle, \
    InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton, Message, InlineQueryResultCachedVideo
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from yt_dlp import YoutubeDL

from bot.app.models import TiktokLink
from bot.handlers.tiktok.text_static import PROCESSING_STARTED
from bot.utils import ECallbackContext


def get_tt_video_info(url: str, download=False) -> str | tuple[str, bytes]:
    result = b''
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            'quiet': True,
            'outtmpl': '%(title).30s-%(id)s.%(ext)s',
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
    with sentry_sdk.start_transaction(op='tt_video_cmd',
                                      name='Download Tiktok video command'):
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
            video_link, video_bytes = get_tt_video_info(source_url,
                                                        download=True)
            update.effective_message.reply_video(video_bytes,
                                                 reply_markup=InlineKeyboardMarkup(
                                                     [
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


def tt_inline_cmd(update: Update, context: ECallbackContext):
    with sentry_sdk.start_transaction(op='tt_inline_cmd',
                                      name='Download Tiktok video inline command'):
        query = update.inline_query.query.strip()

        if not re.match(r'\s*https?://[vmtw.]{0,5}tiktok.com/.*', query):
            return

        logging.debug(f'Processing inline query: {query}')
        tt_cache: TiktokLink = context.db_session.query(TiktokLink).filter(
            or_(TiktokLink.link == query,
                TiktokLink.share_link == query)).one_or_none()
        if tt_cache is None:
            try:
                video_link, video_bytes = get_tt_video_info(query,
                                                            download=True)
            except yt_dlp.utils.DownloadError:
                update.inline_query.answer([])
                return

            # Special chat for uploading video to telegram servers
            special_chat_id = -1001856672797
            video_msg: Message = context.bot.send_video(special_chat_id,
                                                        video_bytes,
                                                        caption=video_link)
            telegram_video_id = video_msg.video.file_id
            context.db_session.add(TiktokLink(link=video_link, share_link=query,
                                              telegram_message_id=telegram_video_id))
            context.db_session.commit()
        else:
            video_link, telegram_video_id = tt_cache.link, tt_cache.telegram_message_id

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

        try:
            update.inline_query.answer(results, cache_time=0)#24 * 60 * 60)
        except BadRequest as e:
            if str(e) == 'Document_invalid':
                context.db_session.delete(tt_cache)
                context.db_session.commit()
                logging.info(f'Invalid video file, deleting from cache')
            else:
                logging.error(f'Error while answering inline query: {str(e)}')
                raise e
