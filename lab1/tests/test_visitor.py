# tests/test_visitor.py
import pytest
from src.Visitor import Visitor
from datetime import datetime

class TestVisitor:
    def test_create_visitor(self):
        visitor = Visitor(name="Алексей", birth_year=1990, gender="м")
        assert visitor.get_name() == "Алексей"
        assert visitor.get_birth_year() == 1990
        assert visitor.get_gender() == "м"

    def test_get_age(self):
        visitor = Visitor(name="Мария", birth_year=2000, gender="ж")
        current_year = datetime.now().year
        assert visitor.get_age() == current_year - 2000

    def test_get_gender_description_male(self):
        visitor = Visitor(name="Пётр", birth_year=1985, gender="м")
        assert visitor.get_gender_description() == "Мужской"

    def test_get_gender_description_female(self):
        visitor = Visitor(name="Ольга", birth_year=1995, gender="ж")
        assert visitor.get_gender_description() == "Женский"

    def test_get_gender_description_unknown(self):
        visitor = Visitor(name="Саша", birth_year=2005, gender="x")
        assert visitor.get_gender_description() == "Не указан"

    def test_get_gender_description_case_insensitive(self):
        visitor1 = Visitor(name="Тест1", birth_year=1990, gender="М")
        visitor2 = Visitor(name="Тест2", birth_year=1990, gender="Ж")
        assert visitor1.get_gender_description() == "Мужской"
        assert visitor2.get_gender_description() == "Женский"

    def test_invalid_birth_year_future(self):
        future_year = datetime.now().year + 10
        with pytest.raises(ValueError):
            Visitor(name="Будущий", birth_year=future_year, gender="м")

    def test_to_dict(self):
        visitor = Visitor(name="Николай", birth_year=1988, gender="м")
        data = visitor.to_dict()
        assert data["name"] == "Николай"
        assert data["birth year"] == 1988
        assert data["gender"] == "м"

    def test_from_dict(self):
        data = {"name": "Елена", "birth year": 1992, "gender": "ж"}
        visitor = Visitor.from_dict(data)
        assert visitor.get_name() == "Елена"
        assert visitor.get_birth_year() == 1992
        assert visitor.get_gender() == "ж"

    def test_serialization_roundtrip(self):
        visitor = Visitor(name="Сергей", birth_year=1980, gender="м")
        data = visitor.to_dict()
        restored = Visitor.from_dict(data)
        assert restored.get_name() == visitor.get_name()
        assert restored.get_birth_year() == visitor.get_birth_year()
        assert restored.get_gender() == visitor.get_gender()