from src.Animal import Animal
from src.Vet import Vet
from datetime import datetime
from typing import Self

class VetLog:
    def __init__(self, animal_id: int, vet_id: int, conclusion: str, date: datetime):
        self._animal_id = animal_id
        self._vet_id = vet_id
        self._conclusion = conclusion
        self._date = date
    
    def get_animal_id(self) -> str:
        return self._animal_id

    def get_vet_id(self) -> str:
        return self._vet_id

    def get_conclusion(self) -> str:
        return self._conclusion

    def get_date(self) -> datetime:
        return self._date
    
    def to_dict(self):
        return {
            "animal id": self.get_animal_id(),
            "vet id": self.get_vet_id(),
            "conclusion": self.get_conclusion(),
            "date": self.get_date().strftime("%d.%m.%Y %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            animal_id=data["animal id"],
            vet_id=data["vet id"],
            conclusion=data["conclusion"],
            date=datetime.strptime(data["date"], "%d.%m.%Y %H:%M:%S")
        )