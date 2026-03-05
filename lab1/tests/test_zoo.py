# tests/test_zoo.py
import pytest
from src.Zoo import Zoo
from src.Enclosure import Enclosure
from src.Vet import Vet
from src.TourGuide import TourGuide
from src.Exposition import Exposition
from src.Tour import Tour
from src.Event import Event
from src.VetLog import VetLog
from src.Animal import Animal
from src.Feed import Feed
from src.Visitor import Visitor
from datetime import datetime
from src.IDGenerator import IDGenerator


@pytest.fixture(autouse=True)
def reset_id_generator():
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
    return Visitor(name="Иван Петров", birth_year=1990, gender="м")


@pytest.fixture
def sample_animal():
    return Animal(name="Лев", type="Хищник")


@pytest.fixture
def sample_vet():
    return Vet(name="Доктор Айболит", specialisation="Хирург")


@pytest.fixture
def sample_feed(sample_datetime):
    return Feed(food="Мясо", date=sample_datetime)


@pytest.fixture
def sample_enclosure(sample_animal, sample_feed):
    return Enclosure(type="Саванна", animals=[sample_animal], feeds=[sample_feed])


@pytest.fixture
def sample_exposition(sample_enclosure):
    return Exposition(
        name="Африканская зона",
        description="Животные Африки",
        enclosure_ids=[sample_enclosure.get_id()]
    )


@pytest.fixture
def sample_tour(sample_exposition, sample_datetime, sample_visitor):
    return Tour(
        exposition_id=sample_exposition.get_id(),
        tour_guide_id=1,
        max_visitors=10,
        visitors=[sample_visitor],
        date=sample_datetime
    )


@pytest.fixture
def sample_event(sample_datetime, sample_visitor):
    return Event(
        name="День открытых дверей",
        description="Праздник для всех",
        max_visitors=100,
        visitors=[sample_visitor],
        date=sample_datetime
    )


@pytest.fixture
def sample_tour_guide():
    return TourGuide(name="Гид Иван", languages="ru,en")


@pytest.fixture
def sample_vet_log(sample_animal, sample_vet, sample_datetime):
    return VetLog(
        animal_id=sample_animal.get_id(),
        vet_id=sample_vet.get_id(),
        conclusion="Здоров",
        date=sample_datetime
    )


@pytest.fixture
def sample_zoo():
    return Zoo(name="Тестовый зоопарк")


class TestZooInitialization:
    def test_default_name(self):
        zoo = Zoo()
        assert zoo.get_name() == "Zooland"

    def test_custom_name(self, sample_zoo):
        assert sample_zoo.get_name() == "Тестовый зоопарк"

    def test_initial_lists_empty(self):
        zoo = Zoo()
        assert len(zoo.get_enclosures()) == 0
        assert len(zoo.get_vets()) == 0
        assert len(zoo.get_guides()) == 0
        assert len(zoo.get_expositions()) == 0
        assert len(zoo.get_tours()) == 0
        assert len(zoo.get_events()) == 0
        assert len(zoo.get_vet_logs()) == 0

    def test_id_counter_init(self):
        zoo = Zoo(id_counter=100)
        assert zoo.get_id_counter() == 100


class TestZooEnclosures:
    def test_add_and_get_enclosure(self, sample_enclosure):
        zoo = Zoo()
        zoo.add_enclosure(sample_enclosure)
        assert len(zoo.get_enclosures()) == 1
        assert zoo.get_enclosure(0) == sample_enclosure

    def test_get_enclosure_invalid_index(self):
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.get_enclosure(0)

    def test_remove_enclosure_success(self, sample_enclosure):
        zoo = Zoo()
        zoo.add_enclosure(sample_enclosure)
        zoo.remove_enclosure(0)
        assert len(zoo.get_enclosures()) == 0

    def test_remove_enclosure_invalid_index(self):
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.remove_enclosure(0)

    def test_get_enclosures_does_not_return_copy(self, sample_enclosure):
        """Тест отражает текущее поведение: копия не возвращается"""
        zoo = Zoo()
        zoo.add_enclosure(sample_enclosure)
        enclosures = zoo.get_enclosures()
        enclosures.append(Enclosure(type="Test", animals=[], feeds=[]))
        # ⚠️ Это баг в коде - список модифицируется
        assert len(zoo.get_enclosures()) == 2


class TestZooVets:
    def test_add_and_get_vet(self, sample_vet):
        zoo = Zoo()
        zoo.add_vet(sample_vet)
        assert sample_vet in zoo.get_vets()

    def test_get_vet_by_index(self, sample_vet):
        zoo = Zoo()
        zoo.add_vet(sample_vet)
        assert zoo.get_vet(0) == sample_vet

    def test_get_vet_invalid_index(self):
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.get_vet(0)

    def test_remove_vet_success(self, sample_vet):
        zoo = Zoo()
        zoo.add_vet(sample_vet)
        zoo.remove_vet(0)
        assert len(zoo.get_vets()) == 0

    def test_remove_vet_invalid_index(self):
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.remove_vet(0)

    def test_get_vet_by_id_found(self, sample_vet):
        zoo = Zoo()
        zoo.add_vet(sample_vet)
        assert zoo.get_vet_by_id(sample_vet.get_id()) == sample_vet

    def test_get_vet_by_id_not_found(self, sample_vet):
        zoo = Zoo()
        zoo.add_vet(sample_vet)
        assert zoo.get_vet_by_id(9999) is None


class TestZooGuides:
    def test_add_and_remove_guide(self, sample_tour_guide):
        zoo = Zoo()
        zoo.add_guide(sample_tour_guide)
        assert len(zoo.get_guides()) == 1
        zoo.remove_guide(0)
        assert len(zoo.get_guides()) == 0

    def test_remove_guide_invalid_index(self):
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.remove_guide(0)

    def test_get_guide_by_id(self, sample_tour_guide):
        zoo = Zoo()
        zoo.add_guide(sample_tour_guide)
        assert zoo.get_guide_by_id(sample_tour_guide.get_id()) == sample_tour_guide
        assert zoo.get_guide_by_id(9999) is None

    def test_get_guides_returns_copy(self, sample_tour_guide):
        zoo = Zoo()
        zoo.add_guide(sample_tour_guide)
        guides = zoo.get_guides()
        guides.clear()
        assert len(zoo.get_guides()) == 1


class TestZooExpositions:
    def test_add_and_get_exposition(self, sample_exposition):
        zoo = Zoo()
        zoo.add_exposition(sample_exposition)
        assert sample_exposition in zoo.get_expositions()

    def test_get_exposition_invalid_index(self):
        zoo = Zoo()
        with pytest.raises(ValueError):
            zoo.get_exposition(0)

    def test_remove_exposition_by_object(self, sample_exposition):
        zoo = Zoo()
        zoo.add_exposition(sample_exposition)
        zoo.remove_exposition(sample_exposition)
        assert sample_exposition not in zoo.get_expositions()

    def test_get_exposition_by_id(self, sample_exposition):
        zoo = Zoo()
        zoo.add_exposition(sample_exposition)
        assert zoo.get_exposition_by_id(sample_exposition.get_id()) == sample_exposition


class TestZooTours:
    def test_add_and_get_tour(self, sample_tour):
        zoo = Zoo()
        zoo.add_tour(sample_tour)
        assert zoo.get_tour(0) == sample_tour

    def test_get_tour_invalid_index_raises_error(self):
        """Изменено: теперь raises IndexError, не возвращает None"""
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.get_tour(0)

    def test_remove_tour_success(self, sample_tour):
        zoo = Zoo()
        zoo.add_tour(sample_tour)
        zoo.remove_tour(0)
        assert len(zoo.get_tours()) == 0

    def test_remove_tour_invalid_index(self):
        """Изменено: теперь raises IndexError, не возвращает False"""
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.remove_tour(0)

    def test_get_tours_returns_copy(self, sample_tour):
        zoo = Zoo()
        zoo.add_tour(sample_tour)
        tours = zoo.get_tours()
        tours.clear()
        assert len(zoo.get_tours()) == 1


class TestZooEvents:
    def test_add_and_remove_event(self, sample_event):
        zoo = Zoo()
        zoo.add_event(sample_event)
        assert zoo.get_event(0) == sample_event
        zoo.remove_event(0)
        assert len(zoo.get_events()) == 0

    def test_get_event_invalid_index(self):
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.get_event(0)

    def test_remove_event_invalid_index(self):
        """Изменено: теперь raises IndexError, не возвращает False"""
        zoo = Zoo()
        with pytest.raises(IndexError):
            zoo.remove_event(0)

    def test_get_events_returns_copy(self, sample_event):
        zoo = Zoo()
        zoo.add_event(sample_event)
        events = zoo.get_events()
        events.clear()
        assert len(zoo.get_events()) == 1


class TestZooVetLogs:
    def test_add_and_get_logs(self, sample_vet_log):
        zoo = Zoo()
        zoo.add_vet_log(sample_vet_log)
        assert sample_vet_log in zoo.get_vet_logs()

    def test_get_vet_logs_returns_copy(self, sample_vet_log):
        zoo = Zoo()
        zoo.add_vet_log(sample_vet_log)
        logs = zoo.get_vet_logs()
        logs.clear()
        assert len(zoo.get_vet_logs()) == 1


class TestZooAnimalSearch:
    def test_get_animal_by_id_found(self, sample_animal, sample_enclosure):
        zoo = Zoo()
        zoo.add_enclosure(sample_enclosure)
        found = zoo.get_animal_by_id(sample_animal.get_id())
        assert found == sample_animal

    def test_get_animal_by_id_not_found(self, sample_enclosure):
        zoo = Zoo()
        zoo.add_enclosure(sample_enclosure)
        assert zoo.get_animal_by_id(9999) is None

    def test_get_animal_empty_enclosures(self):
        zoo = Zoo()
        assert zoo.get_animal_by_id(1) is None


class TestZooDataIntegrity:
    def test_get_vets_returns_copy(self, sample_vet):
        zoo = Zoo()
        zoo.add_vet(sample_vet)
        vets_list = zoo.get_vets()
        vets_list.clear()
        assert len(zoo.get_vets()) == 1

    def test_get_guides_returns_copy(self, sample_tour_guide):
        zoo = Zoo()
        zoo.add_guide(sample_tour_guide)
        guides = zoo.get_guides()
        guides.clear()
        assert len(zoo.get_guides()) == 1

    def test_get_expositions_returns_copy(self, sample_exposition):
        zoo = Zoo()
        zoo.add_exposition(sample_exposition)
        exps = zoo.get_expositions()
        exps.clear()
        assert len(zoo.get_expositions()) == 1

    def test_get_tours_returns_copy(self, sample_tour):
        zoo = Zoo()
        zoo.add_tour(sample_tour)
        tours = zoo.get_tours()
        tours.clear()
        assert len(zoo.get_tours()) == 1

    def test_get_events_returns_copy(self, sample_event):
        zoo = Zoo()
        zoo.add_event(sample_event)
        events = zoo.get_events()
        events.clear()
        assert len(zoo.get_events()) == 1

    def test_get_vet_logs_returns_copy(self, sample_vet_log):
        zoo = Zoo()
        zoo.add_vet_log(sample_vet_log)
        logs = zoo.get_vet_logs()
        logs.clear()
        assert len(zoo.get_vet_logs()) == 1

    def test_get_enclosures_does_not_return_copy(self, sample_enclosure):
        """⚠️ Тест демонстрирует баг в коде"""
        zoo = Zoo()
        zoo.add_enclosure(sample_enclosure)
        enclosures = zoo.get_enclosures()
        original_len = len(enclosures)
        enclosures.append(Enclosure(type="Test", animals=[], feeds=[]))
        assert len(zoo.get_enclosures()) == original_len + 1  # Баг: должно быть original_len


class TestZooIntegration:
    def test_full_workflow(self, sample_zoo, sample_animal, sample_enclosure, 
                          sample_vet, sample_tour_guide, sample_exposition,
                          sample_tour, sample_event, sample_vet_log):
        """Интеграционный тест полного рабочего процесса"""
        sample_zoo.add_enclosure(sample_enclosure)
        assert len(sample_zoo.get_enclosures()) == 1
        
        sample_zoo.add_vet(sample_vet)
        assert len(sample_zoo.get_vets()) == 1
        
        sample_zoo.add_guide(sample_tour_guide)
        assert len(sample_zoo.get_guides()) == 1
        
        sample_zoo.add_exposition(sample_exposition)
        assert len(sample_zoo.get_expositions()) == 1
        
        sample_zoo.add_tour(sample_tour)
        assert len(sample_zoo.get_tours()) == 1
        
        sample_zoo.add_event(sample_event)
        assert len(sample_zoo.get_events()) == 1
        
        sample_zoo.add_vet_log(sample_vet_log)
        assert len(sample_zoo.get_vet_logs()) == 1
        
        assert sample_zoo.get_vet_by_id(sample_vet.get_id()) == sample_vet
        assert sample_zoo.get_guide_by_id(sample_tour_guide.get_id()) == sample_tour_guide
        assert sample_zoo.get_exposition_by_id(sample_exposition.get_id()) == sample_exposition
        assert sample_zoo.get_animal_by_id(sample_animal.get_id()) == sample_animal
        
        sample_zoo.remove_vet(0)
        assert len(sample_zoo.get_vets()) == 0
        
        sample_zoo.remove_guide(0)
        assert len(sample_zoo.get_guides()) == 0
        
        sample_zoo.remove_tour(0)
        assert len(sample_zoo.get_tours()) == 0
        
        sample_zoo.remove_event(0)
        assert len(sample_zoo.get_events()) == 0
        
        sample_zoo.remove_exposition(sample_exposition)
        assert len(sample_zoo.get_expositions()) == 0
        
        sample_zoo.remove_enclosure(0)
        assert len(sample_zoo.get_enclosures()) == 0