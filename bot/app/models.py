from datetime import datetime
from typing import Optional, List

from sqlalchemy import UniqueConstraint, Column, BigInteger
from sqlmodel import SQLModel, Field, Relationship


class GamePlayer(SQLModel, table=True):
    game_id: Optional[int] = Field(default=None, foreign_key="game.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="tguser.id", primary_key=True)

    # user: 'TGUser' = Relationship(back_populates="games")
    # game: 'Game' = Relationship(back_populates="players")
    # winner_at: List['GameResult'] = Relationship(back_populates="winner")


class TGUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tg_id: int = Field(sa_column=Column('tg_id', BigInteger(), nullable=False, index=True, unique=True))
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    lang_code: str = 'en'
    is_blocked: bool = False

    games: List['Game'] = Relationship(back_populates="players", link_model=GamePlayer)
    game_results: List['GameResult'] = Relationship(back_populates="winner")

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 nullable=False)
    last_seen_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    def full_username(self, mention: bool = False, prefix: str = '@'):
        if self.username:
            return (prefix if mention else '') + self.username
        else:
            # Add mention handling with `[{first_name}{" "+last_name}](tg://user?id={tg_id})`
            return self.first_name + (" " + self.last_name if self.last_name else '')


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(sa_column=Column('chat_id', BigInteger(), nullable=False, index=True))

    players: List[TGUser] = Relationship(back_populates="games", link_model=GamePlayer)
    results: List['GameResult'] = Relationship(back_populates="game")


class GameResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    winner_id: int = Field(foreign_key="tguser.id")
    year: int
    day: int

    winner: TGUser = Relationship(back_populates="game_results")
    game: Game = Relationship(back_populates="results")

    __table_args__ = (
        UniqueConstraint('game_id', 'year', 'day', name='unique_game_result'),
    )


class TiktokLink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link: str = Field(index=True)
    share_link: Optional[str] = Field(default=None, index=True)
    # ID of the message with the cached video inside special channel
    telegram_message_id: str

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 nullable=False)


class KVItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(sa_column=Column(BigInteger(), nullable=False, index=True))
    key: str = Field(index=True)
    value: str

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 nullable=False)

    __table_args__ = (
        UniqueConstraint('chat_id', 'key', name='unique_kv_item'),
    )
