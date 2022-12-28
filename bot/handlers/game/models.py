import itertools
import random
from datetime import datetime

import jsons


# TODO: Use database with indexes on fields to improve performance
class Game:
    """Game model"""

    players: list[int] = []
    years: dict[int, dict[int, int]] = {}

    def __init__(self):
        self.players = []
        self.years = {}

    def add_player(self, user_id: int) -> bool:
        if user_id not in self.players:
            self.players.append(user_id)
            return True
        return False

    def remove_player(self, user_id: int):
        self.players.remove(user_id)

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

    def stats_current_year(self) -> dict[int, int]:
        self.ensure_year()
        counter = {}
        for winner in self.years[self.current_year].values():
            counter[winner] = counter.get(winner, 0) + 1
        return counter

    def stats_all_time(self) -> dict[int, int]:
        counter = {}
        for days in self.years.values():
            for winner in days.values():
                counter[winner] = counter.get(winner, 0) + 1
        return counter

    def stats_personal(self, user_id: int) -> int:
        count = 0
        for days in self.years.values():
            for winner in days.values():
                if winner == user_id:
                    count += 1
        return count

    @property
    def current_day(self):
        return datetime.now().day

    @property
    def current_year(self):
        return datetime.now().year

    def to_json(self) -> str:
        return jsons.dumps(self, strip_properties=True)

    @staticmethod
    def from_json(json: str) -> 'Game':
        return jsons.loads(json, Game, strict=True)
