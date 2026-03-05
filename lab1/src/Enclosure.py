import datetime
from src.Animal import Animal
from src.IDGenerator import IDGenerator
from src.Feed import Feed
from typing import Self

class Enclosure:
    def __init__(self, type: str, animals: list[Animal], feeds: list[Feed], id: int = None):
        self._type = type
        self._animals = animals
        self._feeds = feeds

        if id is not None:
            self._id = id
        else:
            self._id = IDGenerator().generate()

    def get_type(self):
        return self._type
    
    def get_id(self):
        return self._id
    
    def get_animals(self):
        return self._animals.copy()
    
    def get_animal(self, i: int):
        if 0 <= i < len(self._animals):
            return self._animals[i]
        else:
            raise IndexError

    def add_animal(self, animal):
        self._animals.append(animal)
    
    def remove_animal(self, i: int):
        if 0 <= i < len(self._animals):
            del self._animals[i]
        else:
            raise IndexError
    
    def feed(self, feed: Feed):
        self._feeds.append(feed)

    def get_feeds(self):
        return self._feeds.copy()

    def clear_feeds(self):
        self._feeds.clear()

    def to_dict(self):
        return {
            "type": self.get_type(),
            "animals": [a.to_dict() for a in self.get_animals()],
            "feeds": [feed.to_dict() for feed in self.get_feeds()],
            "id": self.get_id()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        animals_list = data.get("animals", [])
        if not animals_list:
            animals = []
        else:
            animals = [Animal.from_dict(animal) for animal in animals_list]
        
        feed_list = data.get("feeds", [])
        if not feed_list:
            feeds = []
        else:
            feeds = [Feed.from_dict(feed) for feed in feed_list]

        return cls(
            type=data["type"],
            animals=animals,
            feeds=feeds,
            id=data["id"]
        )