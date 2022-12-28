import random

import requests
from telegram import Update
from telegram.ext import CallbackContext


def meme_cmd(update: Update, _context: CallbackContext):
    try:
        rand_link = 'https://imgflip.com/ajax_img_flip'
        meme_id = requests.get(rand_link).content.decode()[3:]
        update.message.reply_photo(f'https://i.imgflip.com/{meme_id}.jpg')
    except requests.exceptions.RequestException as exception:
        update.message.reply_text('Srry, smth went wrong(')
        raise exception


def memeru_cmd(update: Update, _context: CallbackContext):
    try:
        meme_id = random.randint(2, 21818)
        update.message.reply_photo(f'https://t.me/beobanka/{meme_id}')
    except requests.exceptions.RequestException as exception:
        update.message.reply_text('Srry, smth went wrong(')
        raise exception
