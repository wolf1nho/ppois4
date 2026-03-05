# tests/test_id_generator.py
import pytest
from src.IDGenerator import IDGenerator

class TestIDGenerator:
    def test_singleton_pattern(self):
        """Проверка паттерна Singleton"""
        gen1 = IDGenerator()
        gen2 = IDGenerator()
        assert gen1 is gen2

    def test_generate_incremental_ids(self):
        """ID должны увеличиваться последовательно"""
        gen = IDGenerator()
        id1 = gen.generate()
        id2 = gen.generate()
        id3 = gen.generate()
        assert id1 == 1
        assert id2 == 2
        assert id3 == 3

    def test_get_counter(self):
        """Проверка текущего счетчика"""
        gen = IDGenerator()
        assert gen.get_counter() == 0
        gen.generate()
        assert gen.get_counter() == 1
        gen.generate()
        assert gen.get_counter() == 2

    def test_custom_start_counter(self):
        """Начальное значение счетчика"""
        IDGenerator._instance = None
        IDGenerator._counter = 0
        gen = IDGenerator(start=100)
        assert gen.generate() == 101
        assert gen.get_counter() == 101

    def test_reset_singleton(self):
        """Сброс singleton для тестов"""
        IDGenerator._instance = None
        IDGenerator._counter = 0
        gen = IDGenerator()
        assert gen.generate() == 1