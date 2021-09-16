from telegram import User
from telegram.utils.helpers import escape_markdown


def raw_name(user: User):
    return user.username or user.full_name


def escape_markdown2(text: str):
    return escape_markdown(text, version=2)
