from urllib.parse import quote as urlquote

import requests
from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import raw_name, escape_markdown2


def hello_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text(
        'Hello, {}!'.format(update.message.from_user.first_name))


def slap_cmd(update: Update, context: CallbackContext):
    update.message.reply_markdown_v2(
        r'\**{}* slaps _{}_ around a bit with a large trout'.format(
            raw_name(update.effective_user),
            escape_markdown2(context.args[0]) if context.args else 'void'))


def me_cmd(update: Update, _context: CallbackContext):
    update.message.reply_markdown_v2(
        r'\**{}* {}'.format(
            raw_name(update.effective_user),
            escape_markdown2(update.message.text[4:])))


def shrug_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text(r'¯\_(ツ)_/¯')


def google_cmd(update: Update, _context: CallbackContext):
    query = update.message.text[8:]
    if not query:
        update.message.reply_text('What should I search for?')
    else:
        update.message.reply_text('https://lmgtfy.com/?q=' +
                                  urlquote(update.message.text[8:]),
                                  disable_web_page_preview=True)


def pin_message_cmd(update: Update, _context: CallbackContext):
    if update.message.reply_to_message:
        update.message.reply_to_message.pin()
    else:
        update.message.reply_markdown_v2('reply to message you want to _pin_')


def credits_cmd(update: Update, _context: CallbackContext):
    update.message.reply_markdown_v2(
        "The source code of the bot available via [GitHub repository]"
        "(https://github.com/unaimillan/sublime-telegram-bot)",
        disable_web_page_preview=True)


def meme_cmd(update: Update, _context: CallbackContext):
    try:
        rand_link = 'https://imgflip.com/ajax_img_flip'
        meme_id = requests.get(rand_link).content.decode()[3:]
        update.message.reply_photo(f'https://i.imgflip.com/{meme_id}.jpg')
    except requests.exceptions.RequestException as exception:
        update.message.reply_text('Srry, smth went wrong(')
        raise exception


# Key-Value commands
def get_cmd(update: Update, context: CallbackContext):
    if 'storage' not in context.chat_data:
        update.message.reply_text('no keys yet(')
    elif len(context.args) < 1:
        list_cmd(update, context)
    else:
        update.message.reply_text(
            context.chat_data['storage'].get(context.args[0], 'no such key('))


def list_cmd(update: Update, context: CallbackContext):
    ans = ""
    for (i, (key, value)) in enumerate(
            context.chat_data.get('storage', {}).items()):
        ans += "{}) {} - {}\n".format(i, key, value)
    update.message.reply_text(ans or "no keys yet(")


def set_cmd(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        update.message.reply_text('provide key and value please')
        return
    if 'storage' not in context.chat_data:
        context.chat_data['storage'] = {context.args[0]: context.args[1]}
    else:
        context.chat_data['storage'][context.args[0]] = context.args[1]
    update.message.reply_text(
        'Key {} successfully added'.format(context.args[0]))


def del_cmd(update: Update, context: CallbackContext):
    if 'storage' not in context.chat_data:
        update.message.reply_text('no keys yet(')
    elif len(context.args) < 1:
        update.message.reply_text('give me the keeeey')
    else:
        del context.chat_data['storage'][context.args[0]]
        update.effective_chat.send_message(
            'OK! Key {} successfully deleted'.format(context.args[0]))


def unknown_command_cmd(update: Update, _context: CallbackContext):
    update.effective_message.reply_text(
        "sorry, this command isn't supported yet(")


def echo_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text("{} said {}".format(
        update.effective_user.name,
        update.message.text))


# PIDOR Game
def pidor_cmd(update: Update, _context: CallbackContext):
    update.message.reply_markdown_v2(
        r'хехе, к сожалению {} \- пидор'.format(update.message.from_user.name))


def pidorules_cmd(update: Update, _context: CallbackContext):
    update.message.reply_markdown_v2(
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
        , disable_web_page_preview=True)


def pidoreg_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text('сорре пока не работает, я ушёл спать..😴')
