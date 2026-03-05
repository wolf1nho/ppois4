# tests/test_event.py
import pytest
from src.Event import Event
from src.Visitor import Visitor
from datetime import datetime

class TestEvent:
    def test_create_event(self, sample_visitor, sample_datetime):
        event = Event(
            name="Концерт",
            description="Музыкальное шоу",
            max_visitors=50,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        assert event.get_name() == "Концерт"
        assert event.get_max_visitors() == 50
        assert event.get_visitors_count() == 1

    def test_add_visitor(self, sample_visitor, sample_datetime):
        event = Event(name="Шоу", description="", max_visitors=10, visitors=[], date=sample_datetime)
        event.add_visitor(sample_visitor)
        assert event.get_visitors_count() == 1

    def test_remove_visitor_success(self, sample_visitor, sample_datetime):
        event = Event(name="Шоу", description="", max_visitors=10, visitors=[sample_visitor], date=sample_datetime)
        event.remove_visitor(0)
        assert event.get_visitors_count() == 0

    def test_remove_visitor_invalid_index(self, sample_visitor, sample_datetime):
        event = Event(name="Шоу", description="", max_visitors=10, visitors=[sample_visitor], date=sample_datetime)
        with pytest.raises(IndexError):
            event.remove_visitor(5)

    def test_change_date(self, sample_visitor, sample_datetime):
        event = Event(name="Шоу", description="", max_visitors=10, visitors=[sample_visitor], date=sample_datetime)
        new_date = datetime(2025, 1, 1, 12, 0)
        event.change_date(new_date)
        assert event.get_date() == new_date

    def test_get_visitors_returns_copy(self, sample_visitor, sample_datetime):
        event = Event(name="Шоу", description="", max_visitors=10, visitors=[sample_visitor], date=sample_datetime)
        visitors = event.get_visitors()
        visitors.clear()
        assert event.get_visitors_count() == 1

    def test_to_dict(self, sample_visitor, sample_datetime):
        event = Event(
            name="Фестиваль",
            description="Осенний фестиваль",
            max_visitors=100,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        data = event.to_dict()
        assert data["name"] == "Фестиваль"
        assert data["max visitors"] == 100
        assert "date" in data

    def test_from_dict(self, sample_datetime):
        data = {
            "name": "Выставка",
            "description": "Выставка цветов",
            "max visitors": 200,
            "visitors": [{"name": "Гость", "birth year": 1985, "gender": "м"}],
            "date": sample_datetime.strftime('%d.%m.%Y %H:%M')
        }
        event = Event.from_dict(data)
        assert event.get_name() == "Выставка"
        assert event.get_max_visitors() == 200
        assert event.get_visitors_count() == 1

    def test_from_dict_empty_visitors(self, sample_datetime):
        data = {
            "name": "Пустое событие",
            "description": "",
            "max visitors": 50,
            "visitors": [],
            "date": sample_datetime.strftime('%d.%m.%Y %H:%M')
        }
        event = Event.from_dict(data)
        assert event.get_visitors_count() == 0