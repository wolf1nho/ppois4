import random
from src.Zoo import Zoo
from src.Vet import Vet
from src.Animal import Animal
from src.VetLog import VetLog
from datetime import datetime

class VetService:
    def __init__(self, zoo: Zoo, vet: Vet, animal: Animal):
        self._zoo = zoo
        self._vet_id = vet.get_id()
        self._animal_id = animal.get_id()

    def execute(self):
        if random.random() < 0.15:
            conclusion = "болен"
        else:
            conclusion = "здоров"
        self._zoo.add_vet_log(VetLog(self._animal_id, self._vet_id, conclusion, datetime.now()))
