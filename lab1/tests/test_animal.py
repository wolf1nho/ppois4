# tests/test_animal.py
import pytest
from src.Animal import Animal
from src.IDGenerator import IDGenerator

class TestAnimal:
    def test_create_with_auto_id(self):
        animal = Animal(name="Лев", type="Хищник")
        assert animal.get_name() == "Лев"
        assert animal.get_type() == "Хищник"
        assert animal.get_id() == 1

    def test_create_with_custom_id(self):
        animal = Animal(name="Тигр", type="Хищник", id=999)
        assert animal.get_id() == 999

    def test_to_dict(self):
        animal = Animal(name="Слон", type="Травоядное", id=5)
        data = animal.to_dict()
        assert data["name"] == "Слон"
        assert data["type"] == "Травоядное"
        assert data["id"] == 5

    def test_from_dict(self):
        data = {"name": "Жираф", "type": "Травоядное", "id": 10}
        animal = Animal.from_dict(data)
        assert animal.get_name() == "Жираф"
        assert animal.get_type() == "Травоядное"
        assert animal.get_id() == 10

    def test_serialization_roundtrip(self):
        animal = Animal(name="Зебра", type="Травоядное", id=15)
        data = animal.to_dict()
        restored = Animal.from_dict(data)
        assert restored.get_name() == animal.get_name()
        assert restored.get_type() == animal.get_type()
        assert restored.get_id() == animal.get_id()