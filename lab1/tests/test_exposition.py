# tests/test_exposition.py
import pytest
from src.Exposition import Exposition
from src.exceptions import ExpositionError

class TestExposition:
    def test_create_exposition(self, sample_enclosure):
        exp = Exposition(
            name="Зона хищников",
            description="Львы и тигры",
            enclosure_ids=[sample_enclosure.get_id()]
        )
        assert exp.get_name() == "Зона хищников"
        assert len(exp.get_enclosure_ids()) == 1

    def test_add_enclosure_id(self, sample_enclosure):
        exp = Exposition(name="Тест", description="", enclosure_ids=[])
        exp.add_enclosure(sample_enclosure.get_id())
        assert sample_enclosure.get_id() in exp.get_enclosure_ids()

    def test_add_duplicate_enclosure_raises_error(self, sample_enclosure):
        exp = Exposition(name="Тест", description="", enclosure_ids=[sample_enclosure.get_id()])
        with pytest.raises(ExpositionError):
            exp.add_enclosure(sample_enclosure.get_id())

    def test_remove_enclosure_success(self, sample_enclosure):
        exp = Exposition(name="Тест", description="", enclosure_ids=[sample_enclosure.get_id()])
        exp.remove_enclosure(0)
        assert len(exp.get_enclosure_ids()) == 0

    def test_remove_enclosure_invalid_index(self, sample_enclosure):
        exp = Exposition(name="Тест", description="", enclosure_ids=[sample_enclosure.get_id()])
        with pytest.raises(IndexError):
            exp.remove_enclosure(5)

    def test_get_enclosure_ids_returns_copy(self, sample_enclosure):
        exp = Exposition(name="Тест", description="", enclosure_ids=[sample_enclosure.get_id()])
        ids = exp.get_enclosure_ids()
        ids.clear()
        assert len(exp.get_enclosure_ids()) == 1

    def test_to_dict(self, sample_enclosure):
        exp = Exposition(
            name="Африка",
            description="Африканские животные",
            enclosure_ids=[sample_enclosure.get_id()],
            id=5
        )
        data = exp.to_dict()
        assert data["name"] == "Африка"
        assert data["id"] == 5
        assert "enclosure ids" in data

    def test_from_dict(self):
        data = {
            "name": "Азия",
            "description": "Азиатская зона",
            "enclosure ids": [1, 2, 3],
            "id": 10
        }
        exp = Exposition.from_dict(data)
        assert exp.get_name() == "Азия"
        assert len(exp.get_enclosure_ids()) == 3
        assert exp.get_id() == 10