from urllib.parse import quote as urlquote

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
    update.message.reply_text('https://lmgtfy.com/?q=' + escape_markdown2(
        urlquote(update.message.text[8:])), disable_web_page_preview=True)


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


def pidoreg_cmd(update: Update, _context: CallbackContext):
    update.message.reply_text('сорре пока не работает, я ушёл спать..😴')
