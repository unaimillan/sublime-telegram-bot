from telegram import Update

from bot.app.models import KVItem
from bot.utils import ECallbackContext


# Key-Value commands
def get_cmd(update: Update, context: ECallbackContext):
    if len(context.args) < 1:
        list_cmd(update, context)
        return

    kv_item: KVItem = context.db_session.query(KVItem).filter_by(
        chat_id=update.effective_chat.id, key=context.args[0]).one_or_none()
    if kv_item is None:
        update.message.reply_text('no such key(')
    else:
        update.message.reply_text(kv_item.value)


def list_cmd(update: Update, context: ECallbackContext):
    ans = ""
    items = context.db_session.query(KVItem).filter_by(
        chat_id=update.effective_chat.id).all()
    for i, item in enumerate(items, 1):
        ans += "{}) {} - {}\n".format(i, item.key, item.value)
    # Quick fix to avoid "Message too long" error
    update.message.reply_text(ans[:4000] or "no keys yet(")


def set_cmd(update: Update, context: ECallbackContext):
    if len(context.args) < 2:
        update.message.reply_text('provide key and value please')
        return
    kv_item: KVItem = context.db_session.query(KVItem).filter_by(
        chat_id=update.effective_chat.id,
        key=context.args[0]).one_or_none()
    if kv_item is None:
        kv_item = KVItem(chat_id=update.effective_chat.id,
                         key=context.args[0],
                         value=" ".join(context.args[1:]))
    else:
        kv_item.value = " ".join(context.args[1:])
    context.db_session.add(kv_item)
    context.db_session.commit()
    update.message.reply_text(
        'Key {} successfully added'.format(context.args[0]))


def del_cmd(update: Update, context: ECallbackContext):
    if len(context.args) < 1:
        update.message.reply_text('give me the keeeey')
    kv_item: KVItem = context.db_session.query(KVItem).filter_by(
        chat_id=update.effective_chat.id,
        key=context.args[0]).one_or_none()
    if kv_item is None:
        update.effective_chat.send_message('no such key')
    else:
        context.db_session.delete(kv_item)
        context.db_session.commit()
        update.effective_chat.send_message(
            'OK! Key {} successfully deleted'.format(context.args[0]))
