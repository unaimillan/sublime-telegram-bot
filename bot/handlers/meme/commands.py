import logging
import random

import requests
import telegram.error
from telegram import Update, InlineKeyboardButton, \
    InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import CallbackContext

from bot.handlers.meme.text_callback import MEME_REFRESH, MEMERU_REFRESH


def generate_keyboard(link:str, callback_text: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('🔗', url=link),
        InlineKeyboardButton('🔁', callback_data=callback_text)]])


def get_random_en_meme() -> (str, str):
    if random.randint(0, 1):
        rand_link = 'https://imgflip.com/ajax_img_flip'
        meme_id = requests.get(rand_link).content.decode()[3:]
        meme_link = f'https://i.imgflip.com/{meme_id}.jpg'
        source_link = f'https://imgflip.com/i/{meme_id}'
    else:
        meme_id = random.randint(6, 19791)
        meme_link = f'https://t.me/bestmemes/{meme_id}'
        source_link = meme_link
    return meme_link, source_link


def meme_cmd(update: Update, _context: CallbackContext):
    try:
        meme_link, source_link = get_random_en_meme()
        update.message.reply_photo(meme_link, reply_markup=generate_keyboard(source_link, MEME_REFRESH))
    except requests.exceptions.RequestException as exception:
        update.message.reply_text('Srry, smth went wrong(')
        raise exception


def meme_refresh_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    meme_link, source_link = get_random_en_meme()
    update.effective_message.edit_media(InputMediaPhoto(meme_link),
                               reply_markup=generate_keyboard(source_link,
                                                              MEME_REFRESH))
    query.answer()


ru_meme_channel_list = [
    # ('https://t.me/am_devs/27754'),
    ('https://t.me/beobanka', 2, 21818),
    ('https://t.me/LaQeque', 5, 50781),
    ('https://t.me/paperpublic', 7, 18639),

]


def get_random_ru_meme() -> str:
    channel_link, start, end = random.choice(ru_meme_channel_list)
    meme_id = random.randint(start, end)
    meme_link = f'{channel_link}/{meme_id}'
    return meme_link


# TODO: Add next button and callback_data handles for it
# InlineKeyboardButton('🔁', callback_data='MEMERU_NEXT')
def memeru_cmd(update: Update, _context: CallbackContext):
    meme_link = get_random_ru_meme()
    try:
        update.message.reply_photo(meme_link, reply_markup=generate_keyboard(meme_link, MEMERU_REFRESH))
    except requests.exceptions.RequestException as exception:
        update.message.reply_text('Srry, smth went wrong(')
        raise exception
    except telegram.error.BadRequest as exception:
        logging.debug(f'MEMERU Bad request link: {meme_link}')
        raise exception


def memeru_refresh_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    meme_link = get_random_ru_meme()
    try:
        update.effective_message.edit_media(InputMediaPhoto(meme_link),
                                   reply_markup=generate_keyboard(meme_link,
                                                              MEMERU_REFRESH))
    except requests.exceptions.RequestException as exception:
        logging.warning('HTTP request exception in memeru_refresh_callback')
        update.message.reply_text('Srry, smth went wrong(')
        raise exception
    except telegram.error.BadRequest as exception:
        logging.debug(f'MEMERU Bad request link: {meme_link}')
        raise exception
    query.answer()
