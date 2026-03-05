from typing import Self
from datetime import datetime

class Feed:
    def __init__(self, food: str, date: datetime):
        self._food = food
        self._date = date

    def get_food(self):
        return self._food

    def get_date(self):
        return self._date

    def to_dict(self):
        return {
            "food": self.get_food(),
            "date": self.get_date().strftime('%d.%m.%Y %H:%M')
        }    

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            food=data["food"],
            date=datetime.strptime(data["date"], "%d.%m.%Y %H:%M"),
        )