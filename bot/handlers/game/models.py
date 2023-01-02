import random
from datetime import datetime
from zoneinfo import ZoneInfo

import jsons
from telegram import User

from bot.utils import raw_name

MOSCOW_TZ = ZoneInfo('Europe/Moscow')


# TODO: Use database with indexes on fields to improve performance
class Game:
    """Game model"""

    players: list[int] = []
    player_names: dict[int, str] = {}
    years: dict[int, dict[int, int]] = {}

    def __init__(self):
        self.players = []
        self.player_names = {}
        self.years = {}

    def add_player(self, user: User) -> bool:
        self.player_names[user.id] = raw_name(user)
        if user.id not in self.players:
            self.players.append(user.id)
            return True
        return False

    def remove_player(self, user: User):
        self.player_names[user.id] = raw_name(user)
        if user.id in self.players:
            self.players.remove(user.id)

    def ensure_year(self):
        if self.current_year not in self.years:
            self.years[self.current_year] = {}

    def check_winner(self) -> int | None:
        self.ensure_year()
        if self.current_day in self.years[self.current_year]:
            return self.years[self.current_year][self.current_day]
        else:
            return None

    def play(self) -> int:
        self.ensure_year()
        winner_id = random.choice(self.players)
        self.years[self.current_year][self.current_day] = winner_id
        return winner_id

    def get_sorted_name_count(self, count: dict[int, int]) -> list[(str, int)]:
        names_count = [(self.player_names[user_id], count) for user_id, count in
                       count.items()]
        return sorted(names_count, key=lambda x: x[1], reverse=True)[:50]

    def stats_current_year(self) -> list[(str, int)]:
        self.ensure_year()
        counter = {}
        for winner in self.years[self.current_year].values():
            counter[winner] = counter.get(winner, 0) + 1
        return self.get_sorted_name_count(counter)

    def stats_all_time(self) -> list[(str, int)]:
        counter = {}
        for days in self.years.values():
            for winner in days.values():
                counter[winner] = counter.get(winner, 0) + 1
        return self.get_sorted_name_count(counter)

    def stats_personal(self, user_id: int) -> int:
        count = 0
        for days in self.years.values():
            for winner in days.values():
                if winner == user_id:
                    count += 1
        return count

    @property
    def current_day(self):
        return datetime.now(tz=MOSCOW_TZ).timetuple().tm_yday

    @property
    def current_year(self):
        return datetime.now(tz=MOSCOW_TZ).year

    def to_json(self) -> str:
        return jsons.dumps(self, strip_properties=True)

    @staticmethod
    def from_json(json: str) -> 'Game':
        return jsons.loads(json, Game)
