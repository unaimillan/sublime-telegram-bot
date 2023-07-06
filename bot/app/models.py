from datetime import datetime
from typing import Optional, List

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


class TUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tg_id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    is_blocked: bool = False

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 nullable=False)


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int

    players: List['GamePlayer'] = Relationship(back_populates="game")
    results: List['GameResult'] = Relationship(back_populates="game")


# TODO: Fix this Model for many-to-many relationship
class GamePlayer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    user_id: int = Field(foreign_key="tuser.id")
    active: bool = True

    user: TUser = Relationship(back_populates="players")
    game: Game = Relationship(back_populates="players")
    winner_at: List['GameResult'] = Relationship(back_populates="winner")


class GameResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    winner_id: int = Field(foreign_key="gameplayer.id")
    year: int
    day: int

    winner: GamePlayer = Relationship(back_populates="winner_at")
    game: Game = Relationship(back_populates="results")

    __table_args__ = (
        UniqueConstraint('game_id', 'year', 'day', name='unique_game_result'),
    )


class TiktokLink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link: str
    share_link: Optional[str]
    # ID of the message with the cached video inside special channel
    telegram_message_id: Optional[int]

    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow,
                                 nullable=False)
