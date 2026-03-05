# tests/test_tour_guide.py
import pytest
from src.TourGuide import TourGuide

class TestTourGuide:
    def test_create_with_auto_id(self):
        guide = TourGuide(name="Анна", languages="ru,en")
        assert guide.get_name() == "Анна"
        assert guide.get_languages() == "ru,en"
        assert guide.get_id() == 1

    def test_create_with_custom_id(self):
        guide = TourGuide(name="Борис", languages="de", id=999)
        assert guide.get_id() == 999

    def test_to_dict(self):
        guide = TourGuide(name="Виктор", languages="fr,es", id=5)
        data = guide.to_dict()
        assert data["name"] == "Виктор"
        assert data["languages"] == "fr,es"
        assert data["id"] == 5

    def test_from_dict(self):
        data = {"name": "Галина", "languages": "it", "id": 10}
        guide = TourGuide.from_dict(data)
        assert guide.get_name() == "Галина"
        assert guide.get_languages() == "it"
        assert guide.get_id() == 10

    def test_serialization_roundtrip(self):
        guide = TourGuide(name="Дмитрий", languages="zh", id=15)
        data = guide.to_dict()
        restored = TourGuide.from_dict(data)
        assert restored.get_name() == guide.get_name()
        assert restored.get_languages() == guide.get_languages()
        assert restored.get_id() == guide.get_id()