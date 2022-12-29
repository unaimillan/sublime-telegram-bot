import random

import requests
from telegram import Update, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import CallbackContext


def meme_cmd(update: Update, _context: CallbackContext):
    try:
        if random.randint(0, 1):
            rand_link = 'https://imgflip.com/ajax_img_flip'
            meme_id = requests.get(rand_link).content.decode()[3:]
            meme_link = f'https://i.imgflip.com/{meme_id}.jpg'
            source_link = f'https://imgflip.com/i/{meme_id}'
        else:
            meme_id = random.randint(6, 19791)
            meme_link = f'https://t.me/bestmemes/{meme_id}'
            source_link = meme_link
        update.message.reply_photo(meme_link, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔗', url=source_link)]]))
    except requests.exceptions.RequestException as exception:
        update.message.reply_text('Srry, smth went wrong(')
        raise exception


ru_meme_channel_list = [
    # ('https://t.me/am_devs/27754'),
    ('https://t.me/beobanka', 2, 21818),
    ('https://t.me/LaQeque', 5, 50781),
    ('https://t.me/paperpublic', 7, 18639),

]


# TODO: Add next button and callback_data handles for it
# InlineKeyboardButton('🔁', callback_data='MEMERU_NEXT')
def memeru_cmd(update: Update, _context: CallbackContext):
    try:
        channel_link, start, end = random.choice(ru_meme_channel_list)
        meme_id = random.randint(start, end)
        meme_link = f'{channel_link}/{meme_id}'
        update.message.reply_photo(meme_link, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔗', url=meme_link)]]))
    except requests.exceptions.RequestException as exception:
        update.message.reply_text('Srry, smth went wrong(')
        raise exception
