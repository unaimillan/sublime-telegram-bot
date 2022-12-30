import requests
from telegram import Update
from telegram.ext import CallbackContext


def tt_video_cmd(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ")


tt_headers = {"Accept": "*/*",
              "Accept-Encoding": "identity;q=1, *;q=0",
              "Accept-Language": "en-US;en;q=0.9",
              "Cache-Control": "no-cache",
              "Connection": "keep-alive",
              # "Host": link.split("/")[2], # we split our download link to get    #the server host.
              "Pragma": "no-cache",
              "Range": "bytes=0-",
              "Referer": "https://www.tiktok.com/",
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
              }


def tt_depersonalize_cmd(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text('Not implemented yet')
    return
    tt_link = context.args[0]
    resp = requests.head(tt_link, allow_redirects=True, headers=tt_headers)
    update.effective_message.reply_text(resp.url)
