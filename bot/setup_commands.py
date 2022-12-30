import os

from dotenv import load_dotenv
from telegram import Bot

commands = [
    ('slap', 'simulate /slap command from IRC'),
    ('me', 'simulate /me command from IRC'),
    ('shrug', 'shrug ¯\_(ツ)_/¯'),
    ('google', '<query> let me google that for you'),
    ('get', '<key> get specific entry by key'),
    ('list', 'list entries for current chat'),
    ('set', '<key> <value> set specific value for key'),
    ('del', '<key> remove specific key'),
    ('pidor', 'play the game, see /pidorules first'),
    ('pidorules', 'POTD game rules'),
    ('pidoreg', 'register to the POTD game'),
    ('pidorunreg', 'unregister from the POTD game'),
    ('pidorstats', 'POTD game stats for this year'),
    ('pidorall', 'POTD game stats for all time'),
    ('pidorme', 'POTD personal stats'),
    ('meme', 'get some random meme'),
    ('memeru', 'get some random russian meme'),
    ('ttvideo', 'get video from tiktok'),
    ('ttlink', 'get depersonalized tiktok link'),
    ('about', 'some info about github repo'),
]

if __name__ == '__main__':
    load_dotenv()
    bot = Bot(os.environ['TELEGRAM_BOT_API_SECRET'])
    bot.delete_my_commands()
    # Setup similar commands for both 'en' and 'ru' users
    bot.set_my_commands(commands)
