from sqlmodel import Session
from telegram import User
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

from bot.app.models import TGUser


def raw_name(user: User):
    return user.username or user.full_name


def escape_markdown2(text: str):
    return escape_markdown(text, version=2)


class ECallbackContext(CallbackContext):
    """Extended CallbackContext with additional fields"""
    db_session: Session
    tg_user: TGUser
