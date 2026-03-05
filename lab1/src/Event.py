from src.Visitor import Visitor
from typing import Self
from datetime import datetime

class Event:
    def __init__(self, 
                 name: str, 
                 description: str,
                 max_visitors: int,
                 visitors: list[Visitor],
                 date: datetime):
        self._name = name
        self._description = description
        self._visitors = visitors
        self._max_visitors = max_visitors
        self._date = date
    
    def get_name(self):
        return self._name
    
    def get_description(self):
        return self._description
    
    def get_visitors(self) -> list[Visitor]:
        return self._visitors.copy()

    def get_max_visitors(self):
        return self._max_visitors
    
    def get_visitors_count(self):
        return len(self.get_visitors())

    def get_date(self):
        return self._date
    
    def add_visitor(self, visitor: Visitor):
        self._visitors.append(visitor)

    def change_date(self, date: datetime):
        self._date = date

    def remove_visitor(self, i: int):
        if 0 <= i < len(self._visitors):
            del self._visitors[i]
        else:
            raise IndexError

    def to_dict(self):
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "max visitors": self.get_max_visitors(),
            "visitors": [v.to_dict() for v in self.get_visitors()],
            "date": self.get_date().strftime('%d.%m.%Y %H:%M')
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        visitors_list = data.get("visitors", [])
        if not visitors_list:
            visitors = []
        else:
            visitors = [Visitor.from_dict(visitor) for visitor in visitors_list]

        return cls(
            name=data["name"],
            description=data["description"],
            max_visitors=data["max visitors"],
            visitors=visitors,
            date=datetime.strptime(data["date"], "%d.%m.%Y %H:%M")
        )
