# tests/test_feed.py
import pytest
from src.Feed import Feed
from datetime import datetime

class TestFeed:
    def test_create_feed(self, sample_datetime):
        feed = Feed(food="Сено", date=sample_datetime)
        assert feed.get_food() == "Сено"
        assert feed.get_date() == sample_datetime

    def test_to_dict(self, sample_datetime):
        feed = Feed(food="Трава", date=sample_datetime)
        data = feed.to_dict()
        assert data["food"] == "Трава"
        assert "date" in data

    def test_from_dict(self, sample_datetime):
        data = {
            "food": "Овощи",
            "date": sample_datetime.strftime('%d.%m.%Y %H:%M')
        }
        feed = Feed.from_dict(data)
        assert feed.get_food() == "Овощи"
        assert feed.get_date() == sample_datetime

    def test_serialization_roundtrip(self, sample_datetime):
        feed = Feed(food="Фрукты", date=sample_datetime)
        data = feed.to_dict()
        restored = Feed.from_dict(data)
        assert restored.get_food() == feed.get_food()
        assert restored.get_date() == feed.get_date()