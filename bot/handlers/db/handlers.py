from sqlmodel import Session
from telegram import Update
from telegram.ext import CallbackContext

from bot.app.models import TGUser
from bot.utils import ECallbackContext


def tg_user_middleware_handler(update: Update, context: ECallbackContext):
    session = context.db_session
    tg_user = session.query(TGUser).filter_by(
        tg_id=update.effective_user.id).one_or_none()
    if tg_user is None:
        tg_user = TGUser(tg_id=update.effective_user.id,
                         username=update.effective_user.username,
                         first_name=update.effective_user.first_name,
                         last_name=update.effective_user.last_name,
                         lang_code=update.effective_user.language_code)
        session.add(tg_user)
    else:
        if tg_user.username != update.effective_user.username:
            tg_user.username = update.effective_user.username
        if tg_user.first_name != update.effective_user.first_name:
            tg_user.first_name = update.effective_user.first_name
        if tg_user.last_name != update.effective_user.last_name:
            tg_user.last_name = update.effective_user.last_name
        if tg_user.lang_code != update.effective_user.language_code:
            tg_user.lang_code = update.effective_user.language_code
    session.commit()
    session.refresh(tg_user)
    context.tg_user = tg_user


def open_db_session(db):
    def open_db_session_handler(update: Update, context: ECallbackContext):
        session = Session(db)
        context.db_session = session
    return open_db_session_handler


def close_db_session_handler(update: Update, context: ECallbackContext):
    context.db_session.close()
