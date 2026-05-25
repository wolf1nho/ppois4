from src.IDGenerator import IDGenerator
from typing import Self

class Animal:
    def __init__(self, name: str, type: str, id: int = None):
        self._name = name
        self._type = type

        if id is not None:
            self._id = id
        else:
            self._id = IDGenerator().generate()
    
    def get_name(self):
        return self._name
    
    def get_id(self):
        return self._id
    
    def get_type(self):
        return self._type

    def to_dict(self):
        return {
            "name": self.get_name(),
            "type": self.get_type(),
            "id": self.get_id()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            name=data["name"],
            type=data["type"],
            id=data["id"]
        )