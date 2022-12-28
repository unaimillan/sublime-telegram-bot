from telegram import Update
from telegram.ext import CallbackContext


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
