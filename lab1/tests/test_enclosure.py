# tests/test_enclosure.py
import pytest
from src.Enclosure import Enclosure
from src.Animal import Animal
from src.Feed import Feed
from datetime import datetime

class TestEnclosure:
    def test_create_enclosure(self, sample_animal, sample_feed):
        enc = Enclosure(type="Лес", animals=[sample_animal], feeds=[sample_feed])
        assert enc.get_type() == "Лес"
        assert len(enc.get_animals()) == 1
        assert len(enc.get_feeds()) == 1

    def test_add_animal(self, sample_animal):
        enc = Enclosure(type="Пустыня", animals=[], feeds=[])
        enc.add_animal(sample_animal)
        assert len(enc.get_animals()) == 1

    def test_remove_animal_success(self, sample_animal):
        enc = Enclosure(type="Пустыня", animals=[sample_animal], feeds=[])
        enc.remove_animal(0)
        assert len(enc.get_animals()) == 0

    def test_remove_animal_invalid_index(self, sample_animal):
        enc = Enclosure(type="Пустыня", animals=[sample_animal], feeds=[])
        with pytest.raises(IndexError):
            enc.remove_animal(5)

    def test_get_animal_by_index(self, sample_animal):
        enc = Enclosure(type="Пустыня", animals=[sample_animal], feeds=[])
        assert enc.get_animal(0) == sample_animal

    def test_get_animal_invalid_index(self, sample_animal):
        enc = Enclosure(type="Пустыня", animals=[sample_animal], feeds=[])
        with pytest.raises(IndexError):
            enc.get_animal(5)

    def test_feed_enclosure(self, sample_feed):
        enc = Enclosure(type="Пустыня", animals=[], feeds=[])
        enc.feed(sample_feed)
        assert len(enc.get_feeds()) == 1

    def test_clear_feeds(self, sample_feed):
        enc = Enclosure(type="Пустыня", animals=[], feeds=[sample_feed])
        enc.clear_feeds()
        assert len(enc.get_feeds()) == 0

    def test_get_animals_returns_copy(self, sample_animal):
        enc = Enclosure(type="Пустыня", animals=[sample_animal], feeds=[])
        animals = enc.get_animals()
        animals.clear()
        assert len(enc.get_animals()) == 1

    def test_get_feeds_returns_copy(self, sample_feed):
        enc = Enclosure(type="Пустыня", animals=[], feeds=[sample_feed])
        feeds = enc.get_feeds()
        feeds.clear()
        assert len(enc.get_feeds()) == 1

    def test_to_dict(self, sample_animal, sample_feed):
        enc = Enclosure(type="Саванна", animals=[sample_animal], feeds=[sample_feed], id=5)
        data = enc.to_dict()
        assert data["type"] == "Саванна"
        assert data["id"] == 5
        assert len(data["animals"]) == 1
        assert len(data["feeds"]) == 1

    def test_from_dict(self, sample_datetime):
        data = {
            "type": "Океан",
            "animals": [{"name": "Дельфин", "type": "Млекопитающее", "id": 1}],
            "feeds": [{"food": "Рыба", "date": sample_datetime.strftime('%d.%m.%Y %H:%M')}],
            "id": 10
        }
        enc = Enclosure.from_dict(data)
        assert enc.get_type() == "Океан"
        assert len(enc.get_animals()) == 1
        assert len(enc.get_feeds()) == 1

    def test_from_dict_empty_lists(self):
        data = {"type": "Пусто", "animals": [], "feeds": [], "id": 1}
        enc = Enclosure.from_dict(data)
        assert len(enc.get_animals()) == 0
        assert len(enc.get_feeds()) == 0