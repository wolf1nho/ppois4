# tests/test_vet.py
import pytest
from src.Vet import Vet

class TestVet:
    def test_create_with_auto_id(self):
        vet = Vet(name="Доктор А", specialisation="Терапевт")
        assert vet.get_name() == "Доктор А"
        assert vet.get_specialisation() == "Терапевт"
        assert vet.get_id() == 1

    def test_create_with_custom_id(self):
        vet = Vet(name="Доктор Б", specialisation="Хирург", id=888)
        assert vet.get_id() == 888

    def test_to_dict(self):
        vet = Vet(name="Доктор В", specialisation="Офтальмолог", id=7)
        data = vet.to_dict()
        assert data["name"] == "Доктор В"
        assert data["specialisation"] == "Офтальмолог"
        assert data["id"] == 7

    def test_from_dict(self):
        data = {"name": "Доктор Г", "specialisation": "Невролог", "id": 12}
        vet = Vet.from_dict(data)
        assert vet.get_name() == "Доктор Г"
        assert vet.get_specialisation() == "Невролог"
        assert vet.get_id() == 12

    def test_serialization_roundtrip(self):
        vet = Vet(name="Доктор Д", specialisation="Кардиолог", id=20)
        data = vet.to_dict()
        restored = Vet.from_dict(data)
        assert restored.get_name() == vet.get_name()
        assert restored.get_specialisation() == vet.get_specialisation()
        assert restored.get_id() == vet.get_id()