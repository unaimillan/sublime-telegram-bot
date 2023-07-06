import logging
import os
import pickle

from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

from bot.app.models import TGUser, Game, GameResult, TiktokLink, GamePlayer
from bot.handlers.game.models import Game as RawGame

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL", "Error no db url provided"), echo=True)
raw_data = pickle.load(open("storage/data.bin.backup2", "rb"))
logging.info("All data loaded, sql engine created")

def recreate_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def populate_game():
    session = Session(engine)
    game = Game(chat_id=99)
    session.add(game)
    session.commit()
    session.refresh(game)
    session.close()

def populate_tg_users():
    with Session(engine) as session:
        for tg_id in raw_data['user_data']:
            tguser = TGUser(tg_id=int(tg_id), first_name='undefined')

            session.add(tguser)
            session.commit()

def populate_tiktok_links():
    with Session(engine) as session:
        for short_link, (full_link, tg_key) in raw_data['bot_data']['tiktok_cache'].items():
            link = TiktokLink(link=full_link, share_link=short_link, telegram_message_id=tg_key)
            session.add(link)
            session.commit()


if __name__ == '__main__':
    recreate_db()
    # populate_tiktok_links()
    populate_tg_users()
    populate_game()

    # connection = engine.raw_connection()
    # with open('dump.sql', 'w') as f:
    #     for line in connection.iterdump():
    #         f.write('%s\n' % line)
    # connection.close()
