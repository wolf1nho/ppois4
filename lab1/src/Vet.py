from src.IDGenerator import IDGenerator
from typing import Self

class Vet:
    def __init__(self, name: str, specialisation: str, id: int = None):
        self._name = name
        self._specialisation = specialisation
        
        if id is not None:
            self._id = id
        else:
            self._id = IDGenerator().generate()

    def get_name(self):
        return self._name
    
    def get_id(self):
        return self._id

    def get_specialisation(self):
        return self._specialisation

    # def get_info(self) -> str:
    #     return f"Ветеринар: {self._name}, Специализация: {self._specialisation}"
    
    def to_dict(self):
        return {
            "name": self.get_name(),
            "specialisation": self.get_specialisation(),
            "id": self.get_id()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            name=data["name"],
            specialisation=data["specialisation"],
            id=data["id"]
        )
