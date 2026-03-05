# tests/test_vet_log.py
import pytest
from src.VetLog import VetLog
from datetime import datetime

class TestVetLog:
    def test_create_vet_log(self, sample_datetime):
        log = VetLog(
            animal_id=1,
            vet_id=2,
            conclusion="Здоров",
            date=sample_datetime
        )
        assert log.get_animal_id() == 1
        assert log.get_vet_id() == 2
        assert log.get_conclusion() == "Здоров"
        assert log.get_date() == sample_datetime

    def test_to_dict(self, sample_datetime):
        log = VetLog(
            animal_id=5,
            vet_id=10,
            conclusion="Болен",
            date=sample_datetime
        )
        data = log.to_dict()
        assert data["animal id"] == 5
        assert data["vet id"] == 10
        assert data["conclusion"] == "Болен"
        assert "date" in data

    def test_from_dict(self, sample_datetime):
        data = {
            "animal id": 100,
            "vet id": 200,
            "conclusion": "На лечении",
            "date": sample_datetime.strftime("%d.%m.%Y %H:%M:%S")
        }
        log = VetLog.from_dict(data)
        assert log.get_animal_id() == 100
        assert log.get_vet_id() == 200
        assert log.get_conclusion() == "На лечении"

    def test_serialization_roundtrip(self, sample_datetime):
        log = VetLog(
            animal_id=50,
            vet_id=60,
            conclusion="Профилактика",
            date=sample_datetime
        )
        data = log.to_dict()
        restored = VetLog.from_dict(data)
        assert restored.get_animal_id() == log.get_animal_id()
        assert restored.get_vet_id() == log.get_vet_id()
        assert restored.get_conclusion() == log.get_conclusion()