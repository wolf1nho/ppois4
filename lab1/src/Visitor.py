from datetime import datetime
from typing import Optional
from typing import Self

class Visitor:
    def __init__(self, name: str, birth_year: int, gender: str):
        if birth_year > datetime.now().year:
            raise ValueError
        self._name = name
        self._birth_year = birth_year
        self._gender = gender
    
    def get_name(self):
        return self._name
    
    def get_birth_year(self):
        return self._birth_year
    
    def get_gender(self):
        return self._gender
    
    def get_age(self):
        current_year = datetime.now().year
        return current_year - self._birth_year
    
    def get_gender_description(self):
        if self._gender.lower() == 'м':
            return "Мужской"
        elif self._gender.lower() == 'ж':
            return "Женский"
        else:
            return "Не указан"
    
    def to_dict(self):
        return {
            "name": self.get_name(),
            "birth year": self.get_birth_year(),
            "gender": self.get_gender()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            name=data["name"],
            birth_year=data["birth year"],
            gender=data["gender"]
        )
    
    