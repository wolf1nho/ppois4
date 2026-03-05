# tests/test_vet_service.py
import pytest
from unittest.mock import Mock, patch
from src.VetService import VetService
from datetime import datetime

class TestVetService:
    def test_execute_healthy_conclusion(self, sample_zoo, sample_vet, sample_animal):
        """Тест когда животное здорово (85% вероятность)"""
        with patch('src.VetService.random') as mock_random:
            mock_random.random.return_value = 0.5  # > 0.15 = здоров
            service = VetService(sample_zoo, sample_vet, sample_animal)
            service.execute()
            
            logs = sample_zoo.get_vet_logs()
            assert len(logs) == 1
            assert logs[0].get_conclusion() == "здоров"

    def test_execute_sick_conclusion(self, sample_zoo, sample_vet, sample_animal):
        """Тест когда животное болеет (15% вероятность)"""
        with patch('src.VetService.random') as mock_random:
            mock_random.random.return_value = 0.1  # < 0.15 = болен
            service = VetService(sample_zoo, sample_vet, sample_animal)
            service.execute()
            
            logs = sample_zoo.get_vet_logs()
            assert len(logs) == 1
            assert logs[0].get_conclusion() == "болен"

    def test_execute_stores_correct_ids(self, sample_zoo, sample_vet, sample_animal):
        """Проверка что ID сохраняются корректно"""
        with patch('src.VetService.random') as mock_random:
            mock_random.random.return_value = 0.5
            service = VetService(sample_zoo, sample_vet, sample_animal)
            service.execute()
            
            logs = sample_zoo.get_vet_logs()
            assert logs[0].get_animal_id() == sample_animal.get_id()
            assert logs[0].get_vet_id() == sample_vet.get_id()

    def test_execute_stores_current_datetime(self, sample_zoo, sample_vet, sample_animal):
        """Проверка что дата близка к текущей"""
        with patch('src.VetService.random') as mock_random:
            mock_random.random.return_value = 0.5
            before = datetime.now()
            service = VetService(sample_zoo, sample_vet, sample_animal)
            service.execute()
            after = datetime.now()
            
            logs = sample_zoo.get_vet_logs()
            log_date = logs[0].get_date()
            assert before <= log_date <= after