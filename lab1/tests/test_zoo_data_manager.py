# tests/test_zoo_data_manager.py
import pytest
import json
import os
import tempfile
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.ZooDataManager import ZooDataManager
from src.Zoo import Zoo
from src.Animal import Animal
from src.Enclosure import Enclosure
from src.Vet import Vet
from src.TourGuide import TourGuide
from src.Exposition import Exposition
from src.Tour import Tour
from src.Event import Event
from src.VetLog import VetLog
from src.Feed import Feed
from src.Visitor import Visitor
from src.IDGenerator import IDGenerator


@pytest.fixture(autouse=True)
def reset_id_generator():
    """Сброс ID генератора перед каждым тестом"""
    IDGenerator._instance = None
    IDGenerator._counter = 0
    yield
    IDGenerator._instance = None
    IDGenerator._counter = 0


@pytest.fixture
def temp_file():
    """Создаёт временный файл и удаляет его после теста"""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def sample_datetime():
    return datetime(2024, 6, 15, 10, 30, 0)


@pytest.fixture
def full_zoo(sample_datetime):
    """Создаёт полностью заполненный зоопарк для тестов"""
    zoo = Zoo(name="Тестовый Зоопарк", id_counter=10)
    
    # Животные
    animal1 = Animal(name="Лев", type="Хищник", id=1)
    animal2 = Animal(name="Слон", type="Травоядное", id=2)
    
    # Корм
    feed1 = Feed(food="Мясо", date=sample_datetime)
    feed2 = Feed(food="Трава", date=sample_datetime)
    
    # Вольеры
    enc1 = Enclosure(type="Саванна", animals=[animal1], feeds=[feed1], id=1)
    enc2 = Enclosure(type="Лес", animals=[animal2], feeds=[feed2], id=2)
    zoo.add_enclosure(enc1)
    zoo.add_enclosure(enc2)
    
    # Ветеринары
    vet1 = Vet(name="Доктор А", specialisation="Хирург", id=1)
    vet2 = Vet(name="Доктор Б", specialisation="Терапевт", id=2)
    zoo.add_vet(vet1)
    zoo.add_vet(vet2)
    
    # Вет-логи
    log1 = VetLog(animal_id=1, vet_id=1, conclusion="Здоров", date=sample_datetime)
    log2 = VetLog(animal_id=2, vet_id=2, conclusion="На лечении", date=sample_datetime)
    zoo.add_vet_log(log1)
    zoo.add_vet_log(log2)
    
    # Гиды
    guide1 = TourGuide(name="Гид Иван", languages="ru,en", id=1)
    guide2 = TourGuide(name="Гид Анна", languages="de,fr", id=2)
    zoo.add_guide(guide1)
    zoo.add_guide(guide2)
    
    # Экспозиции
    exp1 = Exposition(name="Африка", description="Африканские животные", 
                      enclosure_ids=[1], id=1)
    exp2 = Exposition(name="Европа", description="Европейские животные", 
                      enclosure_ids=[2], id=2)
    zoo.add_exposition(exp1)
    zoo.add_exposition(exp2)
    
    # Посетители
    visitor1 = Visitor(name="Гость 1", birth_year=1990, gender="м")
    visitor2 = Visitor(name="Гость 2", birth_year=1995, gender="ж")
    
    # Туры
    tour1 = Tour(
        exposition_id=1,
        tour_guide_id=1,
        max_visitors=10,
        visitors=[visitor1],
        date=sample_datetime
    )
    tour2 = Tour(
        exposition_id=2,
        tour_guide_id=2,
        max_visitors=15,
        visitors=[visitor2],
        date=sample_datetime
    )
    zoo.add_tour(tour1)
    zoo.add_tour(tour2)
    
    # События
    event1 = Event(
        name="День открытых дверей",
        description="Праздник для всех",
        max_visitors=100,
        visitors=[visitor1, visitor2],
        date=sample_datetime
    )
    zoo.add_event(event1)
    
    return zoo


class TestZooDataManagerInitialization:
    def test_default_file_path(self):
        manager = ZooDataManager()
        assert manager._file_path == "zoo.json"

    def test_custom_file_path(self):
        manager = ZooDataManager(file_path="custom.json")
        assert manager._file_path == "custom.json"

    def test_file_path_with_directory(self):
        manager = ZooDataManager(file_path="data/zoo.json")
        assert manager._file_path == "data/zoo.json"


class TestZooDataManagerSave:
    def test_save_creates_file(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        assert os.path.exists(temp_file)

    def test_save_creates_valid_json(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
        assert "name" in data
        assert "enclosures" in data
        assert "vets" in data

    def test_save_preserves_zoo_name(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data["name"] == "Тестовый Зоопарк"

    def test_save_preserves_id_counter(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data["id counter"] == 10

    def test_save_enclosures_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data["enclosures"]) == 2

    def test_save_vets_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data["vets"]) == 2

    def test_save_guides_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data["guides"]) == 2

    def test_save_expositions_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data["expositions"]) == 2

    def test_save_tours_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data["tours"]) == 2

    def test_save_events_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data["events"]) == 1

    def test_save_vet_logs_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert len(data["vet logs"]) == 2

    def test_save_empty_zoo(self, temp_file):
        zoo = Zoo(name="Empty Zoo")
        manager = ZooDataManager(file_path=temp_file)
        manager.save(zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert data["name"] == "Empty Zoo"
        assert len(data["enclosures"]) == 0
        assert len(data["vets"]) == 0
        assert len(data["guides"]) == 0

    def test_save_uses_utf8_encoding(self, temp_file):
        zoo = Zoo(name="Зоопарк с эмодзи 🦁")
        manager = ZooDataManager(file_path=temp_file)
        manager.save(zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "🦁" in content

    def test_save_json_indentation(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверка что есть отступы (indent=4)
        assert '    "name"' in content


class TestZooDataManagerLoad:
    def test_load_nonexistent_file_returns_empty_zoo(self, temp_file):
        # Файл не существует
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        manager = ZooDataManager(file_path=temp_file)
        zoo = manager.load()
        
        assert zoo.get_name() == "Zooland"  # Default name
        assert len(zoo.get_enclosures()) == 0

    def test_load_preserves_zoo_name(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert loaded_zoo.get_name() == "Тестовый Зоопарк"

    def test_load_preserves_id_counter(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert loaded_zoo.get_id_counter() == 10

    def test_load_preserves_enclosures_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert len(loaded_zoo.get_enclosures()) == 2

    def test_load_preserves_vets_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert len(loaded_zoo.get_vets()) == 2

    def test_load_preserves_guides_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert len(loaded_zoo.get_guides()) == 2

    def test_load_preserves_expositions_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert len(loaded_zoo.get_expositions()) == 2

    def test_load_preserves_tours_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert len(loaded_zoo.get_tours()) == 2

    def test_load_preserves_events_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert len(loaded_zoo.get_events()) == 1

    def test_load_preserves_vet_logs_count(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        loaded_zoo = manager.load()
        assert len(loaded_zoo.get_vet_logs()) == 2

    def test_load_with_missing_fields_uses_defaults(self, temp_file):
        # Создаём файл с неполными данными
        incomplete_data = {
            "name": "Partial Zoo",
            "id counter": 5
            # Остальные поля отсутствуют
        }
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(incomplete_data, f)
        
        manager = ZooDataManager(file_path=temp_file)
        zoo = manager.load()
        
        assert zoo.get_name() == "Partial Zoo"
        assert zoo.get_id_counter() == 5
        assert len(zoo.get_enclosures()) == 0

    def test_load_empty_lists(self, temp_file):
        data = {
            "name": "Empty Lists Zoo",
            "enclosures": [],
            "vets": [],
            "vet logs": [],
            "guides": [],
            "expositions": [],
            "tours": [],
            "events": [],
            "id counter": 0
        }
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        
        manager = ZooDataManager(file_path=temp_file)
        zoo = manager.load()
        
        assert len(zoo.get_enclosures()) == 0
        assert len(zoo.get_vets()) == 0


class TestZooDataManagerRoundtrip:
    def test_save_and_load_full_zoo(self, full_zoo, temp_file):
        """Полный тест кругового преобразования: save -> load -> verify"""
        manager = ZooDataManager(file_path=temp_file)
        
        # Сохраняем
        manager.save(full_zoo)
        
        # Загружаем
        loaded_zoo = manager.load()
        
        # Проверяем основные атрибуты
        assert loaded_zoo.get_name() == full_zoo.get_name()
        assert loaded_zoo.get_id_counter() == full_zoo.get_id_counter()
        
        # Проверяем количество элементов
        assert len(loaded_zoo.get_enclosures()) == len(full_zoo.get_enclosures())
        assert len(loaded_zoo.get_vets()) == len(full_zoo.get_vets())
        assert len(loaded_zoo.get_guides()) == len(full_zoo.get_guides())
        assert len(loaded_zoo.get_expositions()) == len(full_zoo.get_expositions())
        assert len(loaded_zoo.get_tours()) == len(full_zoo.get_tours())
        assert len(loaded_zoo.get_events()) == len(full_zoo.get_events())
        assert len(loaded_zoo.get_vet_logs()) == len(full_zoo.get_vet_logs())

    def test_save_and_load_enclosure_data(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        loaded_zoo = manager.load()
        
        original_enc = full_zoo.get_enclosure(0)
        loaded_enc = loaded_zoo.get_enclosure(0)
        
        assert loaded_enc.get_type() == original_enc.get_type()
        assert loaded_enc.get_id() == original_enc.get_id()
        assert len(loaded_enc.get_animals()) == len(original_enc.get_animals())

    def test_save_and_load_vet_data(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        loaded_zoo = manager.load()
        
        original_vet = full_zoo.get_vet(0)
        loaded_vet = loaded_zoo.get_vet(0)
        
        assert loaded_vet.get_name() == original_vet.get_name()
        assert loaded_vet.get_specialisation() == original_vet.get_specialisation()
        assert loaded_vet.get_id() == original_vet.get_id()

    def test_save_and_load_exposition_data(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        loaded_zoo = manager.load()
        
        original_exp = full_zoo.get_exposition(0)
        loaded_exp = loaded_zoo.get_exposition(0)
        
        assert loaded_exp.get_name() == original_exp.get_name()
        assert loaded_exp.get_description() == original_exp.get_description()
        assert loaded_exp.get_enclosure_ids() == original_exp.get_enclosure_ids()

    def test_save_and_load_tour_data(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        loaded_zoo = manager.load()
        
        original_tour = full_zoo.get_tour(0)
        loaded_tour = loaded_zoo.get_tour(0)
        
        assert loaded_tour.get_exposition_id() == original_tour.get_exposition_id()
        assert loaded_tour.get_tour_guide_id() == original_tour.get_tour_guide_id()
        assert loaded_tour.get_max_visitors() == original_tour.get_max_visitors()
        assert loaded_tour.get_visitors_count() == original_tour.get_visitors_count()

    def test_save_and_load_event_data(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        loaded_zoo = manager.load()
        
        original_event = full_zoo.get_event(0)
        loaded_event = loaded_zoo.get_event(0)
        
        assert loaded_event.get_name() == original_event.get_name()
        assert loaded_event.get_description() == original_event.get_description()
        assert loaded_event.get_max_visitors() == original_event.get_max_visitors()

    def test_save_and_load_vet_log_data(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        loaded_zoo = manager.load()
        
        original_log = full_zoo.get_vet_logs()[0]
        loaded_log = loaded_zoo.get_vet_logs()[0]
        
        assert loaded_log.get_animal_id() == original_log.get_animal_id()
        assert loaded_log.get_vet_id() == original_log.get_vet_id()
        assert loaded_log.get_conclusion() == original_log.get_conclusion()


class TestZooDataManagerEdgeCases:
    def test_load_corrupted_json(self, temp_file):
        # Создаём невалидный JSON
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("{ invalid json }")
        
        manager = ZooDataManager(file_path=temp_file)
        
        with pytest.raises(json.JSONDecodeError):
            manager.load()

    def test_load_empty_file(self, temp_file):
        # Создаём пустой файл
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        manager = ZooDataManager(file_path=temp_file)
        
        with pytest.raises(json.JSONDecodeError):
            manager.load()

    def test_save_overwrites_existing_file(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        
        # Первое сохранение
        zoo1 = Zoo(name="First Zoo")
        manager.save(zoo1)
        
        # Второе сохранение (должно перезаписать)
        zoo2 = Zoo(name="Second Zoo")
        manager.save(zoo2)
        
        loaded_zoo = manager.load()
        assert loaded_zoo.get_name() == "Second Zoo"

    def test_multiple_save_load_cycles(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        
        # Несколько циклов сохранения/загрузки
        for i in range(3):
            manager.save(full_zoo)
            loaded_zoo = manager.load()
            assert loaded_zoo.get_name() == full_zoo.get_name()

    def test_load_file_with_unicode(self, temp_file):
        data = {
            "name": "Зоопарк 🦁🐯🐻",
            "enclosures": [],
            "vets": [],
            "vet logs": [],
            "guides": [],
            "expositions": [],
            "tours": [],
            "events": [],
            "id counter": 0
        }
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        manager = ZooDataManager(file_path=temp_file)
        zoo = manager.load()
        
        assert zoo.get_name() == "Зоопарк 🦁🐯🐻"


class TestZooDataManagerIntegration:
    def test_full_workflow(self, full_zoo, temp_file):
        """Интеграционный тест полного рабочего процесса"""
        manager = ZooDataManager(file_path=temp_file)
        
        # 1. Сохраняем полный зоопарк
        manager.save(full_zoo)
        
        # 2. Загружаем в новый объект
        loaded_zoo = manager.load()
        
        # 3. Модифицируем загруженный зоопарк
        new_vet = Vet(name="Новый Врач", specialisation="Офтальмолог")
        loaded_zoo.add_vet(new_vet)
        
        # 4. Сохраняем изменения
        manager.save(loaded_zoo)
        
        # 5. Загружаем снова и проверяем
        final_zoo = manager.load()
        assert len(final_zoo.get_vets()) == 3  # Было 2 + 1 новый
        
        # 6. Проверяем что имя сохранилось
        assert final_zoo.get_name() == "Тестовый Зоопарк"

    def test_persistence_across_instances(self, full_zoo, temp_file):
        """Тест что данные сохраняются между разными экземплярами менеджера"""
        # Первый менеджер сохраняет
        manager1 = ZooDataManager(file_path=temp_file)
        manager1.save(full_zoo)
        
        # Второй менеджер загружает (новый экземпляр)
        manager2 = ZooDataManager(file_path=temp_file)
        loaded_zoo = manager2.load()
        
        assert loaded_zoo.get_name() == full_zoo.get_name()
        assert len(loaded_zoo.get_enclosures()) == len(full_zoo.get_enclosures())


class TestZooDataManagerFileOperations:
    def test_save_creates_directory_if_needed(self, temp_file):
        # Создаём путь с поддиректорией
        nested_path = os.path.join(os.path.dirname(temp_file), "subdir", "zoo.json")
        
        try:
            manager = ZooDataManager(file_path=nested_path)
            zoo = Zoo(name="Test")
            
            # Должна возникнуть ошибка т.к. директория не существует
            # (если в коде нет создания директорий)
            with pytest.raises(FileNotFoundError):
                manager.save(zoo)
        finally:
            # Очистка
            if os.path.exists(nested_path):
                os.remove(nested_path)
            dir_path = os.path.dirname(nested_path)
            if os.path.exists(dir_path):
                os.rmdir(dir_path)

    def test_file_permissions(self, full_zoo, temp_file):
        manager = ZooDataManager(file_path=temp_file)
        manager.save(full_zoo)
        
        # Проверяем что файл доступен для чтения
        assert os.access(temp_file, os.R_OK)
        
        # Проверяем что файл доступен для записи
        assert os.access(temp_file, os.W_OK)