from src.Visitor import Visitor
from src.Visitor import Visitor
from typing import Self
from datetime import datetime 

class Tour:
    def __init__(self, exposition_id: int, tour_guide_id: int, max_visitors: int, visitors: list[Visitor], date: datetime):
        self._exposition_id = exposition_id
        self._tour_guide_id = tour_guide_id
        self._visitors = visitors
        self._max_visitors = max_visitors
        self._date = date
    
    def add_visitor(self, visitor: Visitor):
        self._visitors.append(visitor)

    def get_exposition_id(self) -> int:
        return self._exposition_id

    def get_tour_guide_id(self) -> int:
        return self._tour_guide_id

    def get_visitors(self):
        return self._visitors.copy()

    def get_max_visitors(self):
        return self._max_visitors
    
    def get_visitors_count(self):
        return len(self.get_visitors())

    def get_missing_visitors(self):
        return self.get_max_visitors() - self.get_visitors_count()

    def remove_visitor(self, i: int):
        if 0 <= i < len(self._visitors):
            del self._visitors[i]
        else:
            raise IndexError

    def remove_exposition(self, id: int):
        if id == self._exposition_id:
            self._exposition_id = 0

    def get_date(self) -> datetime:
        return self._date

    def change_date(self, date: datetime):
        self._date = date

    def change_exposition_id(self, id: int):
        self._exposition_id = id

    def to_dict(self):
        return {
            "exposition id": self.get_exposition_id(),
            "tour guide id": self.get_tour_guide_id(),
            "date": self.get_date().strftime('%d.%m.%Y %H:%M'),
            "visitors": [v.to_dict() for v in self.get_visitors()],
            "max visitors": self.get_max_visitors()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        visitors_list = data.get("visitors", [])
        if not visitors_list:
            visitors = []
        else:
            visitors = [Visitor.from_dict(visitor) for visitor in visitors_list]

        return cls(
            exposition_id=data["exposition id"],
            tour_guide_id=data["tour guide id"],
            date=datetime.strptime(data["date"], "%d.%m.%Y %H:%M"),
            visitors=visitors,
            max_visitors=data["max visitors"]
        )