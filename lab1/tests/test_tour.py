# tests/test_tour.py
import pytest
from src.Tour import Tour
from src.Visitor import Visitor
from datetime import datetime

class TestTour:
    def test_create_tour(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=15,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        assert tour.get_exposition_id() == 1
        assert tour.get_tour_guide_id() == 2
        assert tour.get_max_visitors() == 15
        assert tour.get_visitors_count() == 1

    def test_add_visitor(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=15,
            visitors=[],
            date=sample_datetime
        )
        tour.add_visitor(sample_visitor)
        assert tour.get_visitors_count() == 1

    def test_remove_visitor_success(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=15,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        tour.remove_visitor(0)
        assert tour.get_visitors_count() == 0

    def test_remove_visitor_invalid_index(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=15,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        with pytest.raises(IndexError):
            tour.remove_visitor(5)

    def test_get_missing_visitors(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=10,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        assert tour.get_missing_visitors() == 9

    def test_change_date(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=10,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        new_date = datetime(2025, 1, 1, 12, 0)
        tour.change_date(new_date)
        assert tour.get_date() == new_date

    def test_change_exposition_id(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=10,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        tour.change_exposition_id(99)
        assert tour.get_exposition_id() == 99

    def test_remove_exposition(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=5,
            tour_guide_id=2,
            max_visitors=10,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        tour.remove_exposition(5)
        assert tour.get_exposition_id() == 0

    def test_remove_exposition_wrong_id(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=5,
            tour_guide_id=2,
            max_visitors=10,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        tour.remove_exposition(99)
        assert tour.get_exposition_id() == 5  # Не изменилось

    def test_get_visitors_returns_copy(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=10,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        visitors = tour.get_visitors()
        visitors.clear()
        assert tour.get_visitors_count() == 1

    def test_to_dict(self, sample_visitor, sample_datetime):
        tour = Tour(
            exposition_id=1,
            tour_guide_id=2,
            max_visitors=10,
            visitors=[sample_visitor],
            date=sample_datetime
        )
        data = tour.to_dict()
        assert data["exposition id"] == 1
        assert data["tour guide id"] == 2
        assert data["max visitors"] == 10

    def test_from_dict(self, sample_datetime):
        data = {
            "exposition id": 5,
            "tour guide id": 3,
            "max visitors": 20,
            "visitors": [{"name": "Гость", "birth year": 1990, "gender": "ж"}],
            "date": sample_datetime.strftime('%d.%m.%Y %H:%M')
        }
        tour = Tour.from_dict(data)
        assert tour.get_exposition_id() == 5
        assert tour.get_tour_guide_id() == 3
        assert tour.get_visitors_count() == 1

    def test_from_dict_empty_visitors(self, sample_datetime):
        data = {
            "exposition id": 1,
            "tour guide id": 1,
            "max visitors": 10,
            "visitors": [],
            "date": sample_datetime.strftime('%d.%m.%Y %H:%M')
        }
        tour = Tour.from_dict(data)
        assert tour.get_visitors_count() == 0