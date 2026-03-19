from src.Zoo import Zoo
from src.Enclosure import Enclosure
from src.VetService import VetService
from src.Animal import Animal
from src.Vet import Vet
from src.TourGuide import TourGuide
from src.Exposition import Exposition
from src.Tour import Tour
from src.Visitor import Visitor
from src.Event import Event
from src.Feed import Feed
from typing import Optional
from datetime import datetime
from src.exceptions import(
    EnclosureError,
    ExpositionError,
    TourError,
    EventError
) 


class ZooMenu:
    def __init__(self, zoo):
        self.zoo: Optional[Zoo] = zoo
    
    def run(self):
        if self.zoo == None:
            self.add_zoo()
        else:
            self.make_choice()

    def make_choice(self):
        while True:
            self.show_menu()
            user_choice = input("Выбор: ")
            match user_choice:
                case "1":
                    self.enclosures_menu()
                case "2":
                    self.staff_menu()
                case "3":
                    self.expositions_menu()
                case "4":
                    self.tours_menu()
                case "5":
                    self.events_menu()
                case "0":
                    print("Выход из программы...")
                    break
                case _:
                    print("Неверный выбор.")

    def show_menu(self):
            print("\n--- Меню ---")
            print("1 - Вольеры")
            print("2 - Коллектив")
            print("3 - Экспозиции")
            print("4 - Экскурсии")
            print("5 - Мероприятия")
            print("0 - Выход")

    def enclosures_menu(self):
        while True: 
            print("\n--- Вольеры ---")
            print("1 - Просмотр вольеров")
            print("2 - Добавить вольер")
            print("3 - Выбор вольера для действия")
            print("4 - Удалить вольер")
            print("0 - Назад")
            
            user_choice = input("Выбор: ")
            match user_choice :
                case "1":
                    self.show_enclosures()
                case "2":
                    self.add_enclosure()
                case "3":
                    try:
                        self.enclosure_menu(self.choose_enclosure())
                    except (EnclosureError, ValueError, IndexError):
                        print("Ошибка")
                case "4":
                    self.remove_enclosure()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def show_enclosures(self):
        enclosures = self.zoo.get_enclosures()
        if not enclosures:
            print("В зоопарке нет вольеров.")
            return
        for i, enclosure in enumerate(enclosures, start=1):
            info = f"Вольер типа '{enclosure.get_type()}'\n"
            info += f"Животных: {len(enclosure.get_animals())}\n"

            if enclosure.get_animals():
                info += "Список животных:\n"
                for animal in enclosure.get_animals():
                    info += f"  - {animal.get_name()} ({animal.get_type()})\n"
            
            print(f"\nВольер №{i}.\n{info}")

    def add_enclosure(self):
        type = input("Тип вольера (например, обычный): ")
        self.zoo.add_enclosure(Enclosure(type,[],[]))

    def remove_enclosure(self):
        if not self.zoo.get_enclosures():
            print("В зоопарке нет вольеров.")
            return
        self.show_enclosures()
        user_choice = int(input("Выберите номер вольера для удаления: "))
        try:
            self.zoo.remove_enclosure(user_choice-1)
            print("Удалено")
        except IndexError:
            print("Ошибка")

    def choose_enclosure(self):
        if not self.zoo.get_enclosures():
            print("Сначала добавьте вольер")
            raise EnclosureError
        self.show_enclosures()
        user_choice = int(input("Выберите номер вольера: "))
        return self.zoo.get_enclosure(user_choice-1)

    def enclosure_menu(self, enclosure: Enclosure):
        while True: 
            print("\n--- Вольер ---")
            print("1 - Просмотр животных")
            print("2 - Медосмотр/лечение животного")
            print("3 - Добавить животное")
            print("4 - Удалить животное")
            print("5 - Покормить животных")
            print("6 - Журнал кормлений")
            print("7 - Очистить журнал кормлений")
            print("0 - Назад")
            
            user_choice = input("Выбор: ")
            match user_choice :
                case "1":
                    self.show_animals(enclosure)
                case "2":
                    self.vet_service(enclosure)
                case "3":    
                    self.add_animal(enclosure)
                case "4":
                    self.remove_animal(enclosure)
                case "5":
                    self.feed(enclosure)
                case "6":
                    self.show_feeds(enclosure)
                case "7":
                    enclosure.clear_feeds()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def show_animals(self, enclosure: Enclosure):
        if not enclosure.get_animals():
            print("В вольере нет животных")
            return 
        for i, animal in enumerate(enclosure.get_animals(), start=1):
            info = f"Имя {animal.get_name()}\n"
            info += f"Вид {animal.get_type()}\n"
            print(f"\nЖивотное №{i}.\n{info}")

    def vet_service(self, enclosure: Enclosure):
        if enclosure.get_animals() and self.zoo.get_vets():
            self.show_animals(enclosure)
            user_choice = int(input("Выберите номер животного для медосмотра/лечения: "))
            animal = enclosure.get_animal(user_choice-1)
            self.show_vets()
            user_choice = int(input("Выберите номер ветеринара для медосмотра/лечения: "))
            vet = self.zoo.get_vet(user_choice-1)
            VetService(self.zoo, vet, animal).execute()

    def show_vets(self):
        vets = self.zoo.get_vets()
        if not vets:
            print("В зоопарке нет ветеринаров")
            return
        for i, vet in enumerate(vets, start=1):
            print(f"\nВетеринар №{i}: {vet.get_name()}, Специализация: {vet.get_specialisation()}")

    def add_animal(self, enclosure: Enclosure):
        type = input("Введите вид животного: ")
        name = input("Введите именя животного: ")
        enclosure.add_animal(Animal(name, type))
        print("Животное добавлено.")

    def remove_animal(self, enclosure: Enclosure):
        if not enclosure.get_animals():
            print("В вольере нет животных")
            return
        self.show_animals(enclosure)
        try:
            user_choice = int(input("Выберите номер животного для удаления: "))
            if enclosure.remove_animal(user_choice-1):
                print("Удалено")
            else:
                print("Ошибка")
        except ValueError:
            print("Введите число.")

    def feed(self, enclosure: Enclosure):
        if not enclosure.get_animals():
            print("В вольере некого кормить")
            return
        self.show_animals(enclosure)
        food = input("Корм: ")
        date_str = input("Дата и время (ДД.ММ.ГГГГ ЧЧ:ММ): ")
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        except ValueError:
            print("Неверный формат даты! Используйте ДД.ММ.ГГГГ ЧЧ:ММ")
            return
        enclosure.feed(Feed(food, date))

    def show_feeds(self, enclosure: Enclosure):
        feeds = enclosure.get_feeds()
        if not feeds:
            print("В этом вольере еще не кормили")
            return
        for i, feed in enumerate(feeds, start=1):
            print(f"\nКормление №{i}.\nКорм: {feed.get_food()}, Дата: {feed.get_date().strftime('%d.%m.%Y %H:%M')}")

    def staff_menu(self):
        while True:
            print("\n--- Коллектив ---")
            print("1 - Экскурсоводы")
            print("2 - Ветеринары")
            print("0 - Назад")

            user_choice = input("Выбор: ")
            match user_choice:
                case "1":
                    self.guide_menu()
                case "2":
                    self.vet_menu()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def vet_menu(self):
        while True:
            print("\n--- Ветеринары ---")
            print("1 - Просмотр списка")
            print("2 - Добавить ветеринара")
            print("3 - Удалить ветеринара")
            print("4 - Просмотр записей медосмотров/лечений")
            print("0 - Назад")

            user_choice = input("Выбор: ")
            match user_choice:
                case "1":
                    self.show_vets()
                case "2":
                    self.add_vet()
                case "3":
                    self.remove_vet()
                case "4":
                    self.show_vet_logs()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def show_vet_logs(self):
        vet_logs = self.zoo.get_vet_logs()
        if not vet_logs:
            print("В зоопарке никого не лечили")
            return
        for i, log in enumerate(vet_logs, start=1):
            animal = self.zoo.get_animal_by_id(log.get_animal_id())
            if animal is not None:
                animal_info = f"{animal.get_name()} ({animal.get_type()})"
            else:
                animal_info = f"ID = {log.get_animal_id()}"
            info = f"\nМедосмотр №{i}.\nЖивотное: {animal_info}\n"
            vet = self.zoo.get_vet_by_id(log.get_vet_id())
            if vet is not None:
                vet_name = vet.get_name()
            else:
                vet_name = f"ID = {log.get_vet_id()}"
            info += f"Ветеринар: {vet_name}\n"
            info += f"Дата: {log.get_date().strftime('%d.%m.%Y %H:%M')}\n"
            info += f"Заключение: {log.get_conclusion()}\n"
            print(info)

    def guide_menu(self):
        while True:
            print("\n--- Экскурсоводы ---")
            print("1 - Просмотр списка")
            print("2 - Добавить экскурсовода")
            print("3 - Удалить экскурсовода")
            print("0 - Назад")

            user_choice = input("Выбор: ")
               
            match user_choice:
                case "1":
                    self.show_guides()
                case "2":
                    self.add_guide()
                case "3":
                    self.remove_guide()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")         

    def add_vet(self):
        name = input("Имя ветеринара: ")
        spec = input("Специализация (например, хирург): ")
        self.zoo.add_vet(Vet(name, spec))
        print("Ветеринар добавлен.")

    def remove_vet(self):
        if not self.zoo.get_vets():
            print("В зоопарке нет ветеринаров")
            return
        self.show_vets()
        try:
            i = int(input("Введите номер ветеринара для удаления: "))
            self.zoo.remove_vet(i - 1)
            print("Удалено")
        except ValueError:
            print("Введите число")
        except IndexError:
            print("Ошибка")

    def show_guides(self):
        guides = self.zoo.get_guides()
        if not guides:
            print("В зоопарке нет экскурсоводов.")
            return
        for i, guide in enumerate(guides, start=1):
            print(f"\nЭкскурсовод №{i}: {guide.get_name()}, Языки: {guide.get_languages()}")

    def add_guide(self):
        name = input("Имя экскурсовода: ")
        langs_input = input("Языки (через запятую, например: русский, английский): ")
        self.zoo.add_guide(TourGuide(name, langs_input))
        print("Экскурсовод добавлен.")

    def remove_guide(self):
        if not self.zoo.get_guides():
            print("В зоопарке нет экскурсоводов.")
            return
        self.show_guides()
        try:
            i = int(input("Введите номер экскурсовода для удаления: "))
            self.zoo.remove_guide(i - 1)
            print("Удалено")
        except ValueError:
            print("Введите число")
        except IndexError:
            print("Ошибка")

    def expositions_menu(self):
        while True:
            print("\n--- Экспозиции ---")
            print("1 - Просмотр списка")
            print("2 - Создать экспозицию")
            print("3 - Выбрать экспозицию для действия")
            print("0 - Назад")
            choice = input("Выбор: ")
            
            match choice:
                case "1":
                    self.show_expositions()
                case "2":
                    self.add_exposition()
                case "3":
                    try:
                        self.exposition_menu(self.choose_exposition())
                    except (ExpositionError, ValueError, IndexError):
                        print("Ошибка")
                case "0":
                    break

    def show_expositions(self):
        if not self.zoo.get_expositions():
            print("В зоопарке нет экспозиций")
            return

        for i, exp in enumerate(self.zoo.get_expositions(), 1):
            info = f"Экспозиция: {exp.get_name()}\n"
            info += f"Описание: {exp.get_description()}\n"
            info += f"Вольеров: {len(exp.get_enclosure_ids())}\n"

            print(f"{i}. {info}")

    def choose_exposition(self):
        if not self.zoo.get_expositions():
            print("Сначала добавьте экспозицию")
            raise ExpositionError
        self.show_expositions()
        user_choice = int(input("Выберите номер экспозиции: "))
        return self.zoo.get_exposition(user_choice-1)

    def add_exposition(self):
        name = input("Название: ")
        desc = input("Описание: ")
        self.zoo.add_exposition(Exposition(name, desc, []))
        print("Экспозиция добавлена.")

    def exposition_menu(self, exp: Exposition):
        while True:
            print(f"\n--- ЭКСПОЗИЦИЯ {exp.get_name()} ---")
            print("1 - Список вольеров")
            print("2 - Добавить вольер")
            print("3 - Удалить вольер")
            print("4 - Удалить экспозицию")
            print("0 - Назад")
            choice = input("Выбор: ")
            
            match choice:
                case "1":
                    self.show_enclosures_in_exposition(exp)
                case "2":
                    self.add_enclosure_to_exposition(exp)
                case "3":
                    self.remove_enclosure_from_exposition(exp)
                case "4":
                    self.remove_exposition(exp)
                    break
                case "0":
                    break

    def remove_exposition(self, exp: Exposition):
        self.zoo.remove_exposition(exp)

    def show_enclosures_in_exposition(self, exp: Exposition):
        ids = exp.get_enclosure_ids()
        if not ids:
            print("В экспозиции нет вольеров")
            return 
        zoo_enclosures = self.zoo.get_enclosures()
        enclosures = [enc for enc in zoo_enclosures if enc.get_id() in ids]
        for i, enclosure in enumerate(enclosures, start=1):
            info = f"Вольер типа '{enclosure.get_type()}'\n"
            info += f"Животных: {len(enclosure.get_animals())}\n"

            if enclosure.get_animals():
                info += "Список животных:\n"
                for animal in enclosure.get_animals():
                    info += f"  - {animal.get_name()} ({animal.get_type()})\n"
            
            print(f"\nВольер №{i}.\n{info}")

    def get_not_added_enclosures(self, exp: Exposition):
        ids = exp.get_enclosure_ids()
        enclosures = self.zoo.get_enclosures()
        not_added_enclosures = [enc for enc in enclosures if enc.get_id() not in ids]
        
        return not_added_enclosures

    def add_enclosure_to_exposition(self, exp: Exposition):
        not_added_enclosures = self.get_not_added_enclosures(exp)
        if not not_added_enclosures:
            print("Ошибка. Вольеры для добавления отсутствуют")
            return
        for i, enclosure in enumerate(not_added_enclosures, start=1):
            info = f"Вольер типа '{enclosure.get_type()}'\n"
            info += f"Животных: {len(enclosure.get_animals())}\n"

            if enclosure.get_animals:
                info += "Список животных:\n"
                for animal in enclosure.get_animals():
                    info += f"  - {animal.get_name()} ({animal.get_type()})\n"
            
            print(f"\nВольер №{i}.\n{info}")
        i = int(input("Введите номер вольера для добавления: "))
        if 0 <= i-1 < len(not_added_enclosures):
            enclosure = not_added_enclosures[i-1]
            exp.add_enclosure(enclosure.get_id())
        else:
            print("Oшибка")

    def remove_enclosure_from_exposition(self, exp: Exposition):
        enclosures = exp.get_enclosure_ids()
        if not enclosures:
            print("В экспозиции нет вольеров")
            return
        ids = exp.get_enclosure_ids()
        zoo_enclosures = self.zoo.get_enclosures()
        enclosures = [enc for enc in zoo_enclosures if enc.get_id() in ids]
        for i, enclosure in enumerate(enclosures, start=1):
            info = f"Вольер типа '{enclosure.get_type()}'\n"
            info += f"Животных: {len(enclosure.get_animals())}\n"

            if enclosure.get_animals():
                info += "Список животных:\n"
                for animal in enclosure.get_animals():
                    info += f"  - {animal.get_name()} ({animal.get_type()})\n"
            
            print(f"\nВольер №{i}.\n{info}")
        try:
            i = int(input("Введите номер вольера для удаления: "))
        except ValueError:
            print("Введите число!")
        try:
            exp.remove_enclosure(i-1)
        except IndexError:
            print("Ошибка")

    def tours_menu(self):
        while True:
            print("\n--- Экскурсии ---")
            print("1 - Список экскурсий")
            print("2 - Добавить экскурсию")
            print("3 - Выбрать экскурсию для действия")
            print("4 - Удалить экскурсию")
            print("0 - Назад")
            
            user_choice = input("Выбор: ")
            match user_choice:
                case "1":
                    self.show_tours()
                case "2":
                    self.add_tour()
                case "3":
                    try:
                        self.tour_menu(self.choose_tour())
                    except (TourError, ValueError, IndexError):
                        print("Ошибка")
                case "4":
                    self.remove_tour()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def show_tours(self):
        tours = self.zoo.get_tours()
        if not tours:
            print("В зоопарке нет экскурсий")
            return 
        for i, tour in enumerate(tours, start=1):
            exp = self.zoo.get_exposition_by_id(tour.get_exposition_id())
            if exp:
                name = exp.get_name()
            else:
                name = f"ID = {tour.get_exposition_id()}"
            info = f"\nЭкскурсия №{i}.\nЭкспозиция: {name}\n"
            guide = self.zoo.get_guide_by_id(tour.get_tour_guide_id())
            if guide:
                name = guide.get_name()
            else:
                name = f"ID = {tour.get_tour_guide_id()}"
            info += f"Экскурсовод: {name}\n"
            info += f"Дата: {tour.get_date().strftime('%d.%m.%Y %H:%M')}\n"
            info += f"Посетителей: {tour.get_visitors_count()}/{tour.get_max_visitors()}"
            print(info)

    def choose_tour(self):
        if not self.zoo.get_tours():
            print("В зоопарке нет экскурсий")
            raise TourError
        self.show_tours()
        user_choice = int(input("Выберите номер экскурсии: "))
        return self.zoo.get_tour(user_choice-1)

    def add_tour(self):
        expositions = self.zoo.get_expositions()
        if not expositions:
            print("В зоопарке нет экспозици")
            return

        print("\nДоступные экспозиции:")
        for i, exp in enumerate(expositions, 1):
            print(f"  {i}. {exp.get_name()}")

        try:
            exp_idx = int(input("Выберите номер экспозиции: "))
            if not (0 <= exp_idx-1 < len(expositions)):
                print("Ошибка")
                return
            exposition = expositions[exp_idx]
        except ValueError:
            print("Введите число!")
            return
        
        guides = self.zoo.get_guides()
        if not guides:
            print("Отсутствуют экскурсоводы")
            return

        print("\nДоступные экскурсоводы:")
        for i, guide in enumerate(guides, 1):
            print(f"  {i}. {guide.get_name()} ({guide.get_languages()})")

        try:
            guide_idx = int(input("Выберите номер экскурсовода: ")) - 1
            if not (0 <= guide_idx < len(guides)):
                print("Неверный номер экскурсовода.")
                return
            tour_guide = guides[guide_idx]
        except ValueError:
            print("Введите число!")
            return

        try:
            max_visitors = int(input("Максимальное количество посетителей: "))
        except ValueError:
            print("Введите число!")
            return 


        date_str = input("Дата и время (ДД.ММ.ГГГГ ЧЧ:ММ): ")
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        except ValueError:
            print("Неверный формат даты! Используйте ДД.ММ.ГГГГ ЧЧ:ММ")
            return

        self.zoo.add_tour(Tour(
            exposition_id=exposition.get_id(),
            tour_guide_id=tour_guide.get_id(),
            visitors=[],
            max_visitors=max_visitors,
            date=date
        ))

        print("\nЭкскурсия успешно создана!")

    def tour_menu(self, tour: Tour):
        while True: 
            print("\n--- Экскурсия ---")
            print("1 - Список посетителей")
            print(f"2 - Добавить посетителя ({tour.get_visitors_count()}/{tour.get_max_visitors()})")
            print("3 - Удалить посетителя")
            print("4 - Перенести экскурсию")
            print("5 - Изменить экспозицию")
            print("6 - Удалить мероприятие")
            print("0 - Назад")
            
            user_choice = input("Выберите операцию: ")
            match user_choice :
                case "1":
                    self.show_visitors(tour)
                case "2":
                    self.add_visitor_to_tour(tour)
                case "3":    
                    self.remove_visitor_from_tour(tour)
                case "4":
                    self.change_tour_date(tour)
                case "5":
                    self.change_exposition(tour)
                case "6":
                    self.remove_tour()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def add_visitor_to_tour(self, tour: Tour):
        name = input("Имя посетителя: ")
        try:
            birth_year = int(input("Год рождения: "))
        except ValueError:
            print("Введите число!")
        sex = input("Пол (м/ж): ")
        tour.add_visitor(Visitor(name, birth_year, sex))
        print("Посетитель добавлен.")

    def remove_visitor_from_tour(self, tour: Tour):
        if tour.get_visitors():
            print("На экскурсию никто не записан")
        self.show_visitors(tour)
        try:
            i = int(input("Введите номер посетителя для удаления: "))
            tour.remove_visitor(i - 1)
            print("Удалено")
        except IndexError:
            print("Ошибка")
        except ValueError:
            print("Введите число!")

    def change_tour_date(self, tour: Event):
        date_str = input("Дата и время (ДД.ММ.ГГГГ ЧЧ:ММ): ")
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        except ValueError:
            print("Неверный формат даты! Используйте ДД.ММ.ГГГГ ЧЧ:ММ")
            return
        
        tour.change_date(date)

    def change_exposition(self, tour: Tour):
        other_expositions = self.zoo.get_expositions()
        for exp in other_expositions:
            if exp.get_id() == tour.get_exposition_id():
                other_expositions.remove(exp)
                break
        if not other_expositions:
            print("Ошибка. Другие экспозиции отсутствуют")
            return
        
        for i, exp in enumerate(other_expositions, start=1):
            info = f"Экспозиция: {exp.get_name()}\n"
            info += f"Описание: {exp.get_description()}\n"
            info += f"Вольеров: {len(exp.get_enclosure_ids())}\n"
            print(f"{i}. {info}")

        i = int(input("Введите номер для добавления: "))
        if 0 <= i-1 < len(other_expositions):
            exp = other_expositions[i-1]
            tour.change_exposition_id(exp.get_id())
        else:
            print("Oшибка")

    def remove_tour(self, tour: Tour):
        self.zoo.remove_tour(tour)

    def remove_tour(self):
        if not self.zoo.get_tours():
            print("В зоопарке нет экскурсий")
            return
        self.show_tours()
        try:
            i = int(input("Введите номер экскурсии для удаления: "))
            if self.zoo.remove_tour(i - 1):
                print("Удалено")
            else:
                print("Ошибка")
        except ValueError:
            print("Введите число!")

    def events_menu(self):
        while True:
            print("\n--- Мероприятия ---")
            print("1 - Список мероприятий")
            print("2 - Добавить мероприятие")
            print("3 - Выбрать мероприятие для действия")
            print("4 - Удалить мероприятие")
            print("0 - Назад")
            
            user_choice = input("Выберите операцию: ")
            match user_choice:
                case "1":
                    self.show_events()
                case "2":
                    self.add_event()
                case "3":
                    try:
                        self.event_menu(self.choose_event())
                    except (EventError, ValueError, IndexError):
                        print("Ошибка")
                case "4":
                    self.remove_event()
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def show_events(self):
        if not self.zoo.get_events():
            print("В зоопарке нет мероприятий")
            return
        
        for i, event in enumerate(self.zoo._events, start=1):
            info = f"Мероприятие: {event.get_name()}\n"
            info += f"Описание: {event.get_description()}\n" 
            info += f"Дата: {event.get_date().strftime('%d.%m.%Y %H:%M')}\n"
            info += f"Посетителей: {event.get_visitors_count()}/{event.get_max_visitors()}"
            print(f"\n№{i}. {info}")
    
    def choose_event(self):
        if self.zoo.get_events():
            print("В зоопарке нет мероприятий")
            raise EventError
        self.show_events()
        user_choice = int(input("Выберите номер мероприятия: "))
        return self.zoo.get_event(user_choice-1)

    def event_menu(self, event: Event):
        while True: 
            print("\n--- Мероприятие ---")
            print("1 - Список посетителей")
            print(f"2 - Добавить посетителя ({event.get_visitors_count()}/{event.get_max_visitors()})")
            print("3 - Удалить посетителя")
            print("4 - Перенести мероприятие")
            print("5 - Удалить мероприятие")
            print("0 - Назад")
            
            user_choice = input("Выберите операцию: ")
            match user_choice:
                case "1":
                    self.show_visitors(event)
                case "2":
                    self.add_visitor_to_event(event)
                case "3":    
                    self.remove_visitor_from_event(event)
                case "4":
                    self.change_event_date(event)
                case "0":
                    break
                case _:
                    print("Неверный выбор.")

    def show_visitors(self, event: Event):
        visitors = event.get_visitors()
        if not visitors:
            print("Нет посетителей")
            return
    
        for i, visitor in enumerate(visitors, 1):
            info = f"Посетитель: {visitor.get_name()}\n"
            info += f"Год рождения: {visitor.get_birth_year()}\n"
            if 0 < visitor.get_age() % 10 < 5:
                age_word = "год"
            else:
                age_word = "лет"
            info += f"Возраст: {visitor.get_age()} {age_word}\n"
            info += f"Пол: {visitor.get_gender_description()}"
            print(f"{i}. {info}")

    def add_event(self):
        name = input("Название: ")
        desc = input("Описание: ")
        max_visitors = int(input("Максимальное количество посетителей: "))
        date_str = input("Дата и время (ДД.ММ.ГГГГ ЧЧ:ММ): ")
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        except ValueError:
            print("Неверный формат даты! Используйте ДД.ММ.ГГГГ ЧЧ:ММ")
            return

        self.zoo.add_event(Event(name, desc, max_visitors, [], date))

    def add_visitor_to_event(self, event: Event):
        name = input("Имя посетителя: ")
        birth_year = int(input("Год рождения: "))
        sex = input("Пол (м/ж): ")
        event.add_visitor(Visitor(name, birth_year, sex))
        print("Посетитель добавлен.")

    def remove_visitor_from_event(self, event: Event):
        self.show_visitors(event)
        try:
            i = int(input("Введите номер посетителя для удаления: "))
            if event.remove_visitor(i - 1):
                print("Удалено")
            else:
                print("Ошибка")
        except ValueError:
            print("Введите число!")

    def change_event_date(self, event: Event):
        date_str = input("Дата и время (ДД.ММ.ГГГГ ЧЧ:ММ): ")
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        except ValueError:
            print("Неверный формат даты! Используйте ДД.ММ.ГГГГ ЧЧ:ММ")
            return
        
        event.change_date(date)

    def remove_event(self):
        if not self.zoo.get_events():
            print("В зоопарке нет мероприятий")
            return
        
        self.show_events()
        try:
            i = int(input("Введите номер мероприятия для удаления: "))
            if self.zoo.remove_event(i - 1):
                print("Удалено")
            else:
                print("Ошибка")
        except ValueError:
            print("Введите число!")
