import random
import time

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from bot.handlers.game.models import Game
from bot.handlers.game.phrases import stage1, stage2, stage3, stage4
from bot.handlers.game.text_static import STATS_PERSONAL, \
    STATS_CURRENT_YEAR, \
    STATS_ALL_TIME, STATS_LIST_ITEM, REGISTRATION_SUCCESS, \
    ERROR_ALREADY_REGISTERED, ERROR_ZERO_PLAYERS, ERROR_NOT_ENOUGH_PLAYERS, \
    REMOVE_REGISTRATION, CURRENT_DAY_GAME_RESULT
from bot.utils import escape_markdown2

GAME_RESULT_TIME_DELAY = 2


# PIDOR Game
def pidor_cmd(update: Update, context: CallbackContext):
    if 'game' in context.chat_data:
        game = Game.from_json(context.chat_data['game'])
    else:
        game = Game()

    if len(game.players) < 2:
        update.effective_chat.send_message(ERROR_NOT_ENOUGH_PLAYERS)
        return

    winner_id: int = game.check_winner()
    if winner_id:
        update.message.reply_markdown_v2(
            CURRENT_DAY_GAME_RESULT.format(
                username=game.player_names[winner_id]))
    else:
        winner_id = game.play()
        update.effective_chat.send_message(random.choice(stage1.phrases))
        time.sleep(GAME_RESULT_TIME_DELAY)
        update.effective_chat.send_message(random.choice(stage2.phrases))
        time.sleep(GAME_RESULT_TIME_DELAY)
        update.effective_chat.send_message(random.choice(stage3.phrases))
        time.sleep(GAME_RESULT_TIME_DELAY)
        update.effective_chat.send_message(random.choice(stage4.phrases).format(
            username='@' + game.player_names[winner_id]))

    context.chat_data['game'] = game.to_json()


def pidorules_cmd(update: Update, _context: CallbackContext):
    update.effective_chat.send_message(
        "Правила игры *Пидор Дня* \(только для групповых чатов\):\n"
        "*1\.* Зарегистрируйтесь в игру по команде */pidoreg*\n"
        "*2\.* Подождите пока зарегиструются все \(или большинство :\)\n"
        "*3\.* Запустите розыгрыш по команде */pidor*\n"
        "*4\.* Просмотр статистики канала по команде */pidorstats*, */pidorall*\n"
        "*5\.* Личная статистика по команде */pidorme*\n"
        "*6\.* Статистика за последний год по комнаде */pidor2020* \(так же есть за 2016\-2020\)\n"
        "*7\. \(\!\!\! Только для администраторов чатов\)*: удалить из игры может только Админ канала, сначала выведя по команде список игроков: */pidormin* list\n"
        "Удалить же игрока можно по команде \(используйте идентификатор пользователя \- цифры из списка пользователей\): */pidormin* del 123456\n"
        "\n"
        "*Важно*, розыгрыш проходит только *раз в день*, повторная команда выведет *результат* игры\.\n"
        "\n"
        "Сброс розыгрыша происходит каждый день в 12 часов ночи по UTC\+2 \(примерно в два часа ночи по Москве\)\.\n\n"
        "Поддержать бота можно по [ссылке](https://github.com/unaimillan/sublime-telegram-bot) :\)"
        , parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


def pidoreg_cmd(update: Update, context: CallbackContext):
    if 'game' in context.chat_data:
        game = Game.from_json(context.chat_data['game'])
    else:
        game = Game()

    if len(game.players) == 0:
        update.effective_chat.send_message(
            ERROR_ZERO_PLAYERS.format(username=update.message.from_user.name))

    if game.add_player(update.message.from_user):
        update.effective_message.reply_markdown_v2(REGISTRATION_SUCCESS)
    else:
        update.effective_message.reply_markdown_v2(ERROR_ALREADY_REGISTERED)

    context.chat_data['game'] = game.to_json()


def pidorunreg_cmd(update: Update, context: CallbackContext):
    if 'game' in context.chat_data:
        game = Game.from_json(context.chat_data['game'])
    else:
        game = Game()

    game.remove_player(update.effective_message.from_user)
    update.effective_message.reply_markdown_v2(REMOVE_REGISTRATION)

    context.chat_data['game'] = game.to_json()


def get_sorted_list_text(player_list: list[(str, int)]) -> str:
    result = []
    for number, (name, amount) in enumerate(player_list, 1):
        result.append(STATS_LIST_ITEM.format(number=number,
                                             username=escape_markdown2(name),
                                             amount=amount))
    return ''.join(result)


def pidorstats_cmd(update: Update, context: CallbackContext):
    if 'game' in context.chat_data:
        game = Game.from_json(context.chat_data['game'])
    else:
        game = Game()

    results = game.stats_current_year()
    player_stats = get_sorted_list_text(results)
    answer = STATS_CURRENT_YEAR.format(player_stats=player_stats,
                                       player_count=len(game.players))
    update.effective_chat.send_message(answer, parse_mode=ParseMode.MARKDOWN_V2)


def pidorall_cmd(update: Update, context: CallbackContext):
    if 'game' in context.chat_data:
        game = Game.from_json(context.chat_data['game'])
    else:
        game = Game()

    results = game.stats_all_time()
    player_stats = get_sorted_list_text(results)
    answer = STATS_ALL_TIME.format(player_stats=player_stats,
                                   player_count=len(game.players))
    update.effective_chat.send_message(answer, parse_mode=ParseMode.MARKDOWN_V2)


def pidorme_cmd(update: Update, context: CallbackContext):
    if 'game' in context.chat_data:
        game = Game.from_json(context.chat_data['game'])
    else:
        game = Game()

    user_id = update.effective_message.from_user.id
    count = game.stats_personal(user_id)
    update.effective_chat.send_message(STATS_PERSONAL.format(
        username=update.effective_user.name, amount=count),
        parse_mode=ParseMode.MARKDOWN_V2)
