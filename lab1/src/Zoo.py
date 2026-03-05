from src.Enclosure import Enclosure
from src.VetLog import VetLog
from src.Vet import Vet
from src.TourGuide import TourGuide
from src.Exposition import Exposition
from src.Tour import Tour
from src.Event import Event
from src.IDGenerator import IDGenerator

class Zoo: 
    def __init__(self, name: str="Zooland", id_counter: int=0):
        self._name = name
        self._enclosures: list[Enclosure] = []
        self._vets: list[Vet] = []
        self._vet_logs: list[VetLog] = []
        self._guides: list[TourGuide] = []
        self._expositions: list[Exposition] = []
        self._tours: list[Tour] = []
        self._events: list[Event] = []
        self._id_generator = IDGenerator(id_counter)

    def get_name(self):
        return self._name

    def get_enclosures(self):
        return self._enclosures

    def get_enclosure(self, i: int):
        if 0 <= i < len(self._enclosures):
            return self._enclosures[i]
        raise IndexError
        
    def get_id_counter(self):
        return self._id_generator.get_counter()

    def add_enclosure(self, enclosure: Enclosure):
        self._enclosures.append(enclosure)

    def remove_enclosure(self, i: int):
        if 0 <= i < len(self._enclosures):
            enclosure_id_to_remove = self._enclosures.pop(i)
        
            for exposition in self._expositions:
                exposition.remove_enclosure(enclosure_id_to_remove)

        else:
            raise IndexError

    def get_expositions(self):
        return self._expositions.copy()

    def add_exposition(self, exp: Exposition):
        self._expositions.append(exp)

    def add_vet(self, vet: Vet):
        self._vets.append(vet)

    def remove_vet(self, i: int):
        if 0 <= i < len(self._vets):
            del self._vets[i]
        else:
            raise IndexError

    def get_vets(self) -> list[Vet]:
        return self._vets.copy()
    
    def get_vet(self, i: int):
        if 0 <= i < len(self._vets):
            return self._vets[i]
        raise IndexError

    def add_guide(self, guide: TourGuide):
        self._guides.append(guide)

    def remove_guide(self, i: int):
        if 0 <= i < len(self._guides):
            del self._guides[i]
        else:
            raise IndexError

    def get_guides(self) -> list[TourGuide]:
        return self._guides.copy()

    def get_vet_logs(self):
        return self._vet_logs.copy()
    
    def add_vet_log(self, log: VetLog):
        self._vet_logs.append(log)

    def get_exposition(self, i: int):
        if 0 <= i < len(self._expositions):
            return self._expositions[i]
        raise ValueError

    def remove_exposition(self, exp: Exposition):
        self._expositions.remove(exp)

    def get_tours(self):
        return self._tours.copy()
    
    def get_tour(self, i: int):
        if 0 <= i < len(self._tours):
            return self._tours[i]
        raise IndexError
    
    def add_tour(self, tour: Tour):
        self._tours.append(tour)

    def remove_tour(self, i: int):
        if 0 <= i < len(self._tours):
            del self._tours[i]
        else:
            raise IndexError
    
    def get_events(self):
        return self._events.copy()

    def add_event(self, e: Event):
        self._events.append(e)

    def get_event(self, i: int):
        if 0 <= i < len(self._events):
            return self._events[i]
        else:
            raise IndexError

    def remove_event(self, i: int):
        if 0 <= i < len(self._events):
            del self._events[i]
        else:
            raise IndexError

    def get_exposition_by_id(self, id: int):
        for exposition in self.get_expositions():
            if exposition.get_id() == id:
                return exposition
            
    def get_guide_by_id(self, id: int):
        for guide in self.get_guides():
            if guide.get_id() == id:
                return guide
            
    def get_vet_by_id(self, id: int):
        for vet in self.get_vets():
            if vet.get_id() == id:
                return vet
            
    def get_animal_by_id(self, id: int):
        for enc in self.get_enclosures():
            for animal in enc.get_animals():
                if animal.get_id() == id:
                    return animal