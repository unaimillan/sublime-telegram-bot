from telegram.ext import Dispatcher, CommandHandler, Filters, \
    CallbackQueryHandler

from bot.handlers.about.commands import about_cmd
from bot.handlers.game.commands import pidor_cmd, pidorules_cmd, pidoreg_cmd, \
    pidorunreg_cmd, pidorstats_cmd, pidorall_cmd, pidorme_cmd
from bot.handlers.kvstore.commands import get_cmd, set_cmd, del_cmd, list_cmd
from bot.handlers.meme.commands import meme_cmd, memeru_cmd, \
    meme_refresh_callback, memeru_refresh_callback
from bot.handlers.meme.text_callback import MEME_REFRESH, MEMERU_REFRESH
from bot.handlers.misc.commands import hello_cmd, echo_cmd, slap_cmd, me_cmd, \
    shrug_cmd, google_cmd, pin_message_cmd
from bot.handlers.misc.error import bot_error_handler
from bot.handlers.tiktok.commands import tt_video_cmd, tt_depersonalize_cmd


# TODO: Refactor this function to automatically scan for handlers ending with
#  '_cmd' in the bot/handlers folder
def init_dispatcher(dp: Dispatcher):
    """Register handlers."""
    ne = ~Filters.update.edited_message

    # About handler
    dp.add_handler(CommandHandler('about', about_cmd, filters=ne))

    # Tiktok handlers
    dp.add_handler(CommandHandler('ttvideo', tt_video_cmd, filters=ne))
    dp.add_handler(CommandHandler('ttlink', tt_depersonalize_cmd, filters=ne))

    # Meme handlers
    dp.add_handler(CommandHandler('meme', meme_cmd, filters=ne))
    dp.add_handler(CallbackQueryHandler(meme_refresh_callback, pattern=MEME_REFRESH))
    dp.add_handler(CommandHandler('memeru', memeru_cmd, filters=ne))
    dp.add_handler(CallbackQueryHandler(memeru_refresh_callback, pattern=MEMERU_REFRESH))

    # Game handlers
    dp.add_handler(CommandHandler('pidor', pidor_cmd, filters=ne))
    dp.add_handler(
        CommandHandler('pidorules', pidorules_cmd, filters=ne))
    dp.add_handler(CommandHandler('pidoreg', pidoreg_cmd, filters=ne))
    dp.add_handler(CommandHandler('pidorunreg', pidorunreg_cmd, filters=ne))
    dp.add_handler(CommandHandler('pidorstats', pidorstats_cmd, filters=ne))
    dp.add_handler(CommandHandler('pidorall', pidorall_cmd, filters=ne))
    dp.add_handler(CommandHandler('pidorme', pidorme_cmd, filters=ne))

    # Key-Value storage handlers
    dp.add_handler(CommandHandler('get', get_cmd, filters=ne))
    dp.add_handler(CommandHandler('list', list_cmd, filters=ne))
    dp.add_handler(CommandHandler('set', set_cmd, filters=ne))
    dp.add_handler(CommandHandler('del', del_cmd, filters=ne))

    # Misc handlers
    dp.add_handler(CommandHandler("hello", hello_cmd, filters=ne))
    dp.add_handler(CommandHandler("echo", echo_cmd, filters=ne))
    dp.add_handler(CommandHandler('slap', slap_cmd, filters=ne))
    dp.add_handler(CommandHandler('me', me_cmd, filters=ne))
    dp.add_handler(CommandHandler('shrug', shrug_cmd, filters=ne))
    dp.add_handler(CommandHandler('google', google_cmd, filters=ne))
    dp.add_handler(CommandHandler('pin', pin_message_cmd, filters=ne))

    dp.add_error_handler(bot_error_handler)
