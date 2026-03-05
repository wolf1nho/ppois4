from src.IDGenerator import IDGenerator
from typing import Self

class TourGuide:
    def __init__(self, name: str, languages: str, id: int = None):
        self._name = name
        self._languages = languages
        if id is not None:
            self._id = id
        else:
            self._id = IDGenerator().generate()

    # def get_info(self) -> str:
    #     return f"Экскурсовод: {self.get_name()}, Языки: {self.get_languages()}"
    
    def get_id(self):
        return self._id
    
    def get_name(self):
        return self._name
    
    def get_languages(self):
        return self._languages
    
    def to_dict(self):
        return {
            "name": self.get_name(),
            "languages": self.get_languages(),
            "id": self.get_id()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            name=data["name"],
            languages=data["languages"],
            id=data["id"]
        )