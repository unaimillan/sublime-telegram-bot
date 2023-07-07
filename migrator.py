import asyncio
import logging
import os
import pickle

from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from telethon import TelegramClient

from bot.app.models import TGUser, Game, GameResult, TiktokLink, GamePlayer, \
    KVItem
from bot.handlers.game.models import Game as RawGame

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL", "Error no db url provided"), echo=False)
# raw_data = pickle.load(open("storage/data.bin", "rb"))
raw_data = pickle.load(open("storage/data.bin.backup2", "rb"))
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

async def get_user_id_info(client, tg_ids: [int]):
    # me = await client.get_me()
    # print(me.stringify())
    for tg_id in tg_ids:
        user = await client.get_entity(tg_id)
        await asyncio.sleep(0.25)
        with Session(engine) as session:
            tguser = session.query(TGUser).filter(TGUser.tg_id == tg_id).one()
            tguser.username = user.username
            tguser.first_name = user.first_name
            tguser.last_name = user.last_name
            tguser.lang_code = user.lang_code
            session.commit()
            session.refresh(tguser)
            print(tguser)


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
                game_player = GamePlayer(game_id=game.id, user_id=player)
                session.add(game_player)
            for year in raw_game.years:
                for day, winner in raw_game.years[year].items():
                    game_result = GameResult(game_id=game.id, year=year, day=day, winner_id=winner)
                    session.add(game_result)
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
    # tg_user_ids = populate_tg_users()
    # populate_game()

    # client = TelegramClient('test', int(os.environ['TG_API_ID']),
    #                         os.environ['TG_API_HASH'])
    # with client:
    #     client.loop.run_until_complete(get_user_id_info(client, [267726592]))

    # connection = engine.raw_connection()
    # with open('dump.sql', 'w') as f:
    #     for line in connection.iterdump():
    #         f.write('%s\n' % line)
    # connection.close()
