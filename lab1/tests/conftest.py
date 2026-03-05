# tests/conftest.py
import pytest
from datetime import datetime
import sys
import os

# Добавляем корень проекта в path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.IDGenerator import IDGenerator

@pytest.fixture(autouse=True)
def reset_id_generator():
    """Сбрасываем счетчик ID перед каждым тестом для изоляции"""
    IDGenerator._instance = None
    IDGenerator._counter = 0
    yield
    IDGenerator._instance = None
    IDGenerator._counter = 0

@pytest.fixture
def sample_datetime():
    return datetime(2024, 6, 15, 10, 30)

@pytest.fixture
def sample_visitor():
    from src.Visitor import Visitor
    return Visitor(name="Иван Петров", birth_year=1990, gender="м")

@pytest.fixture
def sample_animal():
    from src.Animal import Animal
    return Animal(name="Лев", type="Хищник")

@pytest.fixture
def sample_vet():
    from src.Vet import Vet
    return Vet(name="Доктор Айболит", specialisation="Хирург")

@pytest.fixture
def sample_feed(sample_datetime):
    from src.Feed import Feed
    return Feed(food="Мясо", date=sample_datetime)

@pytest.fixture
def sample_enclosure(sample_animal, sample_feed):
    from src.Enclosure import Enclosure
    return Enclosure(
        type="Саванна",
        animals=[sample_animal],
        feeds=[sample_feed]
    )

@pytest.fixture
def sample_exposition(sample_enclosure):
    from src.Exposition import Exposition
    return Exposition(
        name="Африканская зона",
        description="Животные Африки",
        enclosure_ids=[sample_enclosure.get_id()]
    )

@pytest.fixture
def sample_tour(sample_exposition, sample_datetime, sample_visitor):
    from src.Tour import Tour
    return Tour(
        exposition_id=sample_exposition.get_id(),
        tour_guide_id=1,
        max_visitors=10,
        visitors=[sample_visitor],
        date=sample_datetime
    )

@pytest.fixture
def sample_event(sample_datetime, sample_visitor):
    from src.Event import Event
    return Event(
        name="День открытых дверей",
        description="Праздник для всех",
        max_visitors=100,
        visitors=[sample_visitor],
        date=sample_datetime
    )

@pytest.fixture
def sample_tour_guide():
    from src.TourGuide import TourGuide
    return TourGuide(name="Гид Иван", languages="ru,en")

@pytest.fixture
def sample_vet_log(sample_animal, sample_vet, sample_datetime):
    from src.VetLog import VetLog
    return VetLog(
        animal_id=sample_animal.get_id(),
        vet_id=sample_vet.get_id(),
        conclusion="Здоров",
        date=sample_datetime
    )

@pytest.fixture
def sample_zoo():
    from src.Zoo import Zoo
    return Zoo(name="Тестовый зоопарк")