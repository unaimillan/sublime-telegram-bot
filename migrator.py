import asyncio
import logging
import os
import pickle
from typing import List

from dotenv import load_dotenv
from sqlalchemy import func, text
from sqlmodel import create_engine, Session, SQLModel, select
from telethon import TelegramClient

from bot.app.models import TGUser, Game, GameResult, TiktokLink, GamePlayer, \
    KVItem
from bot.handlers.game.models import Game as RawGame

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL", "Error no db url provided"), echo=False)
# raw_data = pickle.load(open("storage/data.bin", "rb"))
raw_data = pickle.load(open("storage/data.bin.backup4", "rb"))
logging.info("All data loaded, sql engine created")


def recreate_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def populate_tg_users() -> list[int]:
    players = set()
    chats = []
    for chat_id, chat_data in raw_data['chat_data'].items():
        if chat_id < 0:
            chats.append(chat_id)
        if len(chat_data) <= 0:
            continue
        raw_game = RawGame.from_json(chat_data['game'])
        players |= set(raw_game.players)
        players |= set(raw_game.player_names.keys())
    print("Game users:", len(players))
    print("Bot users:", len(raw_data['user_data']))
    users = players.union(set(raw_data['user_data']))
    print("Total users:", len(users))

    with Session(engine) as session:
        for tg_id in users:
            tguser = TGUser(tg_id=int(tg_id), first_name='undefined')
            session.add(tguser)
            session.commit()
    return list(users)


async def get_user_id_info(client):
    # me = await client.get_me()
    # print(me.stringify())
    with Session(engine) as session:
        games: List[Game] = session.query(Game).filter(Game.chat_id < 0).all()
        for game in games:
            try:
                chat_users = await client.get_participants(game.chat_id)
            except ValueError:
                chat_users = []
                print(f'Chat {game.chat_id} failed to retrieve, processing..')
            print(f'Chat {game.chat_id} retrieved with {len(chat_users)} users')
            await asyncio.sleep(2)
            for chat_user in chat_users:
                maybe_user = session.query(TGUser).filter_by(tg_id=chat_user.id).all()
                for db_user in maybe_user:
                    # tg_user = await client.get_entity(db_user.tg_id)
                    db_user.username = chat_user.username
                    db_user.first_name = chat_user.first_name or '<undefined>'
                    db_user.last_name = chat_user.last_name
                    db_user.lang_code = chat_user.lang_code or 'en'
                    session.commit()
                    session.refresh(db_user)
                    print(db_user)


def populate_game():
    with Session(engine) as session:
        for game_id, game_data in raw_data['chat_data'].items():
            if len(game_data) <= 0:
                continue
            raw_game = RawGame.from_json(game_data['game'])
            game = Game(chat_id=game_id)
            session.add(game)
            session.commit()
            session.refresh(game)
            for player in raw_game.players:
                game.players.append(session.query(TGUser).filter_by(tg_id=player).one())
            session.commit()
            for year in raw_game.years:
                for day, winner_tg_id in raw_game.years[year].items():
                    winner: TGUser = session.query(TGUser).filter_by(tg_id=winner_tg_id).one()
                    winner.game_results.append(GameResult(game_id=game.id, year=year, day=day))
                    session.add(winner)
            session.commit()


def populate_tiktok_links():
    with Session(engine) as session:
        for short_link, (full_link, tg_key) in raw_data['bot_data']['tiktok_cache'].items():
            link = TiktokLink(link=full_link, share_link=short_link, telegram_message_id=tg_key)
            session.add(link)
            session.commit()


def populate_kv_items():
    with Session(engine) as session:
        for chat_id, chat_data in raw_data['chat_data'].items():
            if 'storage' in chat_data:
                for k, v in chat_data['storage'].items():
                    link = KVItem(chat_id=int(chat_id), key=k, value=v)
                    session.add(link)
        session.commit()


if __name__ == '__main__':
    recreate_db()
    # populate_tiktok_links()
    populate_kv_items()
    tg_user_ids = populate_tg_users()
    populate_game()

    # with Session(engine) as session:
    #     tg_id = 123456
    #     user: TGUser = session.query(TGUser).filter_by(tg_id=tg_id).one()
    #     game: Game = session.query(Game).filter_by(id=1).one()
    #     session.add(GameResult(game=game, winner_id=user.id, year=2020, day=1))
    #     print(user.full_username())
    #     print(user.games)
    #     print(len(game.players))
    #     stmt = select(TGUser, func.count(GameResult.winner_id).label('count')) \
    #         .join(TGUser, GameResult.winner_id == TGUser.id) \
    #         .filter(GameResult.game_id == 2, GameResult.year == 2023) \
    #         .group_by(TGUser) \
    #         .order_by(text('count DESC'))
    #     db_results = session.exec(stmt).all()
    #     print(*db_results, sep='\n')

    # client = TelegramClient('sublimebothelper', int(os.environ['TG_API_ID']),
    #                         os.environ['TG_API_HASH']).start(bot_token=os.environ['TELEGRAM_BOT_API_SECRET'])
    #
    # with client:
    #     client.loop.run_until_complete(get_user_id_info(client))

    # connection = engine.raw_connection()
    # with open('dump.sql', 'w') as f:
    #     for line in connection.iterdump():
    #         f.write('%s\n' % line)
    # connection.close()
