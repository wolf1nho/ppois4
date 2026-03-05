from src.Enclosure import Enclosure
from src.IDGenerator import IDGenerator
from typing import Self
from src.exceptions import ExpositionError

class Exposition:
    def __init__(self, name: str, description: str, enclosure_ids: list[int], id: int = None):
        self._name = name
        self._description = description
        self._enclosure_ids = enclosure_ids
        if id is not None:
            self._id = id
        else:
            self._id = IDGenerator().generate()
    
    def get_name(self) -> str:
        return self._name
    
    def get_id(self):
        return self._id

    def get_description(self) -> str:
        return self._description
    
    def add_enclosure(self, enclosure_id: int):
        if enclosure_id not in self._enclosure_ids:
            self._enclosure_ids.append(enclosure_id)
        else:
            raise ExpositionError()
    
    def remove_enclosure(self, i: int):
        if 0 <= i < len(self._enclosure_ids):
            del self._enclosure_ids[i]
        else:
            raise IndexError
    
    def get_enclosure_ids(self):
        return self._enclosure_ids.copy()

    def to_dict(self):
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "enclosure ids":self.get_enclosure_ids(),
            "id":self.get_id()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            name=data["name"],
            description=data["description"],
            enclosure_ids=data["enclosure ids"],
            id=data["id"]
        )