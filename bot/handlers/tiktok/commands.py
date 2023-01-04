import tempfile

import yt_dlp.utils
from telegram import Update
from telegram.ext import CallbackContext
from yt_dlp import YoutubeDL


def get_tt_video(url: str) -> bytes:
    result = b''
    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            # 'quiet': True,
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
    elif update.effective_message.reply_to_message and len(update.effective_message.reply_to_message.text) > 10:
        source_url = update.effective_message.reply_to_message.text
    else:
        update.effective_message.reply_text(
            "Provide a TikTok link after the command or reply to the link")
        return

    try:
        update.effective_message.reply_video(get_tt_video(source_url))
    except yt_dlp.utils.DownloadError:
        update.effective_chat.send_message(
            'Failed to process the link, please, try another one')


def get_tt_source_url(url: str) -> str:
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return info['webpage_url'].replace(info['uploader_id'],
                                           info['uploader'])


def tt_depersonalize_cmd(update: Update, context: CallbackContext) -> None:
    if context.args and len(context.args) == 1:
        source_url = context.args[0]
    elif update.effective_message.reply_to_message and len(update.effective_message.reply_to_message.text) > 10:
        source_url = update.effective_message.reply_to_message.text
    else:
        update.effective_message.reply_text(
            "Provide a TikTok link after the command or reply to the link")
        return

    try:
        update.effective_chat.send_message(get_tt_source_url(source_url))
    except yt_dlp.utils.DownloadError:
        update.effective_chat.send_message(
            'Failed to process the link, please, try another one')
