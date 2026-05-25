from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from src.Animal import Animal
from src.Enclosure import Enclosure
from src.Event import Event
from src.Exposition import Exposition
from src.Feed import Feed
from src.Tour import Tour
from src.TourGuide import TourGuide
from src.Vet import Vet
from src.VetService import VetService
from src.Visitor import Visitor
from src.ZooDataManager import ZooDataManager

DATA_PATH = 'zoo.json'


def _load_zoo():
    return ZooDataManager(DATA_PATH).load()


def _save_zoo(zoo):
    ZooDataManager(DATA_PATH).save(zoo)


def _parse_dt(value: str):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M')


def _base_context(zoo, error=None):
    return {'zoo': zoo, 'error': error}


def _idx(raw: str, upper: int, label: str) -> int:
    i = int(raw)
    if not (0 <= i < upper):
        raise ValueError(f'{label}: некорректный выбор')
    return i


def index(request: HttpRequest) -> HttpResponse:
    return redirect('enclosures')


def enclosures_page(request: HttpRequest) -> HttpResponse:
    zoo = _load_zoo()
    error = None

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'add_enclosure':
                enc_type = request.POST['enc_type'].strip()
                if not enc_type:
                    raise ValueError('Тип вольера не может быть пустым')
                if any(e.get_type().lower() == enc_type.lower() for e in zoo.get_enclosures()):
                    raise ValueError('Вольер такого типа уже существует')
                zoo.add_enclosure(Enclosure(enc_type, [], []))
            elif action == 'remove_enclosure':
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                zoo.remove_enclosure(enc_index)
            elif action == 'add_animal':
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                enc = zoo.get_enclosure(enc_index)
                animal_name = request.POST['animal_name'].strip()
                animal_type = request.POST['animal_type'].strip()
                if not animal_name or not animal_type:
                    raise ValueError('Имя и вид животного обязательны')
                if any(a.get_name().lower() == animal_name.lower() for a in enc.get_animals()):
                    raise ValueError('Животное с таким именем уже есть в этом вольере')
                enc.add_animal(Animal(animal_name, animal_type))
            elif action == 'remove_animal':
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                animal_index = _idx(request.POST['animal_index'], len(zoo.get_enclosure(enc_index).get_animals()), 'Животное')
                zoo.get_enclosure(enc_index).remove_animal(animal_index)
            elif action == 'feed_enclosure':
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                enc = zoo.get_enclosure(enc_index)
                if not enc.get_animals():
                    raise ValueError('Нельзя кормить пустой вольер')
                enc.feed(Feed(request.POST['food'], _parse_dt(request.POST['feed_date'])))
            elif action == 'clear_feeds':
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                enc = zoo.get_enclosure(enc_index)
                if not enc.get_feeds():
                    raise ValueError('Журнал кормлений уже пуст')
                enc.clear_feeds()
            _save_zoo(zoo)
            return redirect('enclosures')
        except Exception as exc:
            error = str(exc)

    enclosures = zoo.get_enclosures()
    context = _base_context(zoo, error)
    context['page'] = 'enclosures'
    context['enclosures'] = list(enumerate(enclosures))
    context['enclosure_choices'] = [
        (i, f"{enc.get_type()} (животных: {len(enc.get_animals())})") for i, enc in enumerate(enclosures)
    ]
    context['enclosure_animal_choices'] = [
        (f"{enc_i}:{animal_i}", f"{enc.get_type()} -> {animal.get_name()} ({animal.get_type()})")
        for enc_i, enc in enumerate(enclosures)
        for animal_i, animal in enumerate(enc.get_animals())
    ]
    context['enclosures_with_animals'] = [
        {
            'enc_index': enc_i,
            'enc_label': f"{enc.get_type()} (животных: {len(enc.get_animals())})",
            'animals': [
                {'animal_index': animal_i, 'label': f"{animal.get_name()} ({animal.get_type()})"}
                for animal_i, animal in enumerate(enc.get_animals())
            ],
        }
        for enc_i, enc in enumerate(enclosures)
        if enc.get_animals()
    ]
    context['clearable_feed_enclosures'] = [
        (enc_i, f"{enc.get_type()} (кормлений: {len(enc.get_feeds())})")
        for enc_i, enc in enumerate(enclosures)
        if enc.get_feeds()
    ]
    return render(request, 'zoo_web/enclosures.html', context)


def staff_page(request: HttpRequest) -> HttpResponse:
    zoo = _load_zoo()
    error = None

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'add_vet':
                name = request.POST['vet_name'].strip()
                spec = request.POST['vet_spec'].strip()
                if not name or not spec:
                    raise ValueError('Имя и специализация ветеринара обязательны')
                if any(v.get_name().lower() == name.lower() for v in zoo.get_vets()):
                    raise ValueError('Ветеринар с таким именем уже существует')
                zoo.add_vet(Vet(name, spec))
            elif action == 'remove_vet':
                vet_index = _idx(request.POST['vet_index'], len(zoo.get_vets()), 'Ветеринар')
                zoo.remove_vet(vet_index)
            elif action == 'add_guide':
                name = request.POST['guide_name'].strip()
                langs = request.POST['guide_langs'].strip()
                if not name or not langs:
                    raise ValueError('Имя и языки экскурсовода обязательны')
                if any(g.get_name().lower() == name.lower() for g in zoo.get_guides()):
                    raise ValueError('Экскурсовод с таким именем уже существует')
                zoo.add_guide(TourGuide(name, langs))
            elif action == 'remove_guide':
                guide_index = _idx(request.POST['guide_index'], len(zoo.get_guides()), 'Экскурсовод')
                zoo.remove_guide(guide_index)
            elif action == 'vet_service':
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                animal_index = _idx(request.POST['animal_index'], len(zoo.get_enclosure(enc_index).get_animals()), 'Животное')
                animal = zoo.get_enclosure(enc_index).get_animal(animal_index)
                vet_index = _idx(request.POST['vet_index'], len(zoo.get_vets()), 'Ветеринар')
                vet = zoo.get_vet(vet_index)
                VetService(zoo, vet, animal).execute()
            _save_zoo(zoo)
            return redirect('staff')
        except Exception as exc:
            error = str(exc)

    vets = zoo.get_vets()
    guides = zoo.get_guides()
    enclosures = zoo.get_enclosures()

    context = _base_context(zoo, error)
    context['page'] = 'staff'
    context['vets'] = list(enumerate(vets))
    context['guides'] = list(enumerate(guides))
    context['vet_choices'] = [(i, f"{vet.get_name()} ({vet.get_specialisation()})") for i, vet in enumerate(vets)]
    context['guide_choices'] = [(i, f"{guide.get_name()} ({guide.get_languages()})") for i, guide in enumerate(guides)]
    context['enclosure_animal_choices'] = [
        (f"{enc_i}:{animal_i}", f"{enc.get_type()} -> {animal.get_name()} ({animal.get_type()})")
        for enc_i, enc in enumerate(enclosures)
        for animal_i, animal in enumerate(enc.get_animals())
    ]
    context['enclosures_with_animals'] = [
        {
            'enc_index': enc_i,
            'enc_label': f"{enc.get_type()} (животных: {len(enc.get_animals())})",
            'animals': [
                {'animal_index': animal_i, 'label': f"{animal.get_name()} ({animal.get_type()})"}
                for animal_i, animal in enumerate(enc.get_animals())
            ],
        }
        for enc_i, enc in enumerate(enclosures)
    ]
    return render(request, 'zoo_web/staff.html', context)


def vet_logs_page(request: HttpRequest) -> HttpResponse:
    zoo = _load_zoo()
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'clear_vet_logs':
            if not zoo.get_vet_logs():
                return redirect('vet_logs')
            zoo.clear_vet_logs()
            _save_zoo(zoo)
            return redirect('vet_logs')
        if action == 'vet_service':
            try:
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                animal_index = _idx(request.POST['animal_index'], len(zoo.get_enclosure(enc_index).get_animals()), 'Животное')
                vet_index = _idx(request.POST['vet_index'], len(zoo.get_vets()), 'Ветеринар')
                animal = zoo.get_enclosure(enc_index).get_animal(animal_index)
                vet = zoo.get_vet(vet_index)
                VetService(zoo, vet, animal).execute()
                _save_zoo(zoo)
                return redirect('vet_logs')
            except Exception:
                pass

    rows = []
    for log in zoo.get_vet_logs():
        animal = zoo.get_animal_by_id(log.get_animal_id())
        vet = zoo.get_vet_by_id(log.get_vet_id())
        rows.append(
            {
                'animal': f'{animal.get_name()} ({animal.get_type()})' if animal else 'Неизвестное животное',
                'vet': vet.get_name() if vet else 'Неизвестный ветеринар',
                'date': log.get_date(),
                'conclusion': log.get_conclusion(),
            }
        )

    context = _base_context(zoo, None)
    context['page'] = 'vet_logs'
    context['rows'] = rows
    context['vet_choices'] = [(i, f"{vet.get_name()} ({vet.get_specialisation()})") for i, vet in enumerate(zoo.get_vets())]
    context['enclosures_with_animals'] = [
        {
            'enc_index': enc_i,
            'enc_label': f"{enc.get_type()} (животных: {len(enc.get_animals())})",
            'animals': [
                {'animal_index': animal_i, 'label': f"{animal.get_name()} ({animal.get_type()})"}
                for animal_i, animal in enumerate(enc.get_animals())
            ],
        }
        for enc_i, enc in enumerate(zoo.get_enclosures())
    ]
    return render(request, 'zoo_web/vet_logs.html', context)


def expositions_page(request: HttpRequest) -> HttpResponse:
    zoo = _load_zoo()
    error = None

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'add_exposition':
                name = request.POST['exp_name'].strip()
                desc = request.POST['exp_desc'].strip()
                if not name or not desc:
                    raise ValueError('Название и описание экспозиции обязательны')
                if any(exp.get_name().lower() == name.lower() for exp in zoo.get_expositions()):
                    raise ValueError('Экспозиция с таким названием уже существует')
                zoo.add_exposition(Exposition(name, desc, []))
            elif action == 'remove_exposition':
                exp_index = _idx(request.POST['exp_index'], len(zoo.get_expositions()), 'Экспозиция')
                zoo.remove_exposition(zoo.get_exposition(exp_index))
            elif action == 'add_enclosure_to_exposition':
                exp_index = _idx(request.POST['exp_index'], len(zoo.get_expositions()), 'Экспозиция')
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                exp = zoo.get_exposition(exp_index)
                enc = zoo.get_enclosure(enc_index)
                if enc.get_id() in exp.get_enclosure_ids():
                    raise ValueError('Этот вольер уже добавлен в выбранную экспозицию')
                exp.add_enclosure(enc.get_id())
            elif action == 'remove_enclosure_from_exposition':
                exp_index = _idx(request.POST['exp_index'], len(zoo.get_expositions()), 'Экспозиция')
                exp = zoo.get_exposition(exp_index)
                enc_pos = _idx(request.POST['enc_pos'], len(exp.get_enclosure_ids()), 'Вольер в экспозиции')
                exp.remove_enclosure(enc_pos)
            _save_zoo(zoo)
            return redirect('expositions')
        except Exception as exc:
            error = str(exc)

    expositions = zoo.get_expositions()
    enclosures = zoo.get_enclosures()

    context = _base_context(zoo, error)
    context['page'] = 'expositions'
    context['expositions'] = list(enumerate(expositions))
    context['exposition_choices'] = [(i, exp.get_name()) for i, exp in enumerate(expositions)]
    context['enclosure_choices'] = [(i, f"{enc.get_type()} (животных: {len(enc.get_animals())})") for i, enc in enumerate(enclosures)]

    context['expositions_with_enclosures'] = []
    context['expositions_with_available_enclosures'] = []
    for exp_i, exp in enumerate(expositions):
        ids = exp.get_enclosure_ids()
        attached = [enc for enc in enclosures if enc.get_id() in ids]
        ids_set = set(ids)
        removable = [
            {'enc_pos': pos, 'label': f"{enc.get_type()} (животных: {len(enc.get_animals())})"}
            for pos, enc in enumerate(attached)
        ]
        addable = [
            {'enc_index': enc_i, 'label': f"{enc.get_type()} (животных: {len(enc.get_animals())})"}
            for enc_i, enc in enumerate(enclosures)
            if enc.get_id() not in ids_set
        ]
        if removable:
            context['expositions_with_enclosures'].append(
                {
                    'exp_index': exp_i,
                    'exp_label': exp.get_name(),
                    'enclosures': removable,
                }
            )
        if addable:
            context['expositions_with_available_enclosures'].append(
                {
                    'exp_index': exp_i,
                    'exp_label': exp.get_name(),
                    'enclosures': addable,
                }
            )

    return render(request, 'zoo_web/expositions.html', context)


def tours_page(request: HttpRequest) -> HttpResponse:
    zoo = _load_zoo()
    error = None

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'add_tour':
                exp_index = _idx(request.POST['exp_index'], len(zoo.get_expositions()), 'Экспозиция')
                guide_index = _idx(request.POST['guide_index'], len(zoo.get_guides()), 'Экскурсовод')
                exp = zoo.get_exposition(exp_index)
                guide = zoo.get_guides()[guide_index]
                max_vis = int(request.POST['tour_max'])
                if max_vis < 1:
                    raise ValueError('Максимум посетителей должен быть больше 0')
                zoo.add_tour(Tour(exp.get_id(), guide.get_id(), max_vis, [], _parse_dt(request.POST['tour_date'])))
            elif action == 'remove_tour':
                tour_index = _idx(request.POST['tour_index'], len(zoo.get_tours()), 'Экскурсия')
                zoo.remove_tour(tour_index)
            elif action == 'change_tour_date':
                tour_index = _idx(request.POST['tour_index'], len(zoo.get_tours()), 'Экскурсия')
                tour = zoo.get_tour(tour_index)
                tour.change_date(_parse_dt(request.POST['tour_date']))
            elif action == 'change_tour_exposition':
                tour_index = _idx(request.POST['tour_index'], len(zoo.get_tours()), 'Экскурсия')
                exp_index = _idx(request.POST['exp_index'], len(zoo.get_expositions()), 'Экспозиция')
                tour = zoo.get_tour(tour_index)
                exp = zoo.get_exposition(exp_index)
                
                # ЗАЩИТА: Проверка совпадения экспозиции
                if exp.get_id() == tour.get_exposition_id():
                    raise ValueError('Эта экспозиция уже выбрана для данной экскурсии')
                    
                tour.change_exposition_id(exp.get_id())
            elif action == 'change_tour_guide':
                tour_index = _idx(request.POST['tour_index'], len(zoo.get_tours()), 'Экскурсия')
                guide_index = _idx(request.POST['guide_index'], len(zoo.get_guides()), 'Экскурсовод')
                tour = zoo.get_tour(tour_index)
                guide = zoo.get_guides()[guide_index]
                
                # ЗАЩИТА: Проверка совпадения гида
                if guide.get_id() == tour.get_tour_guide_id():
                    raise ValueError('Этот экскурсовод уже назначен на данную экскурсию')
                    
                tour.change_tour_guide_id(guide.get_id())
            elif action == 'add_visitor_to_tour':
                tour_index = _idx(request.POST['tour_index'], len(zoo.get_tours()), 'Экскурсия')
                tour = zoo.get_tour(tour_index)
                vis_name = request.POST['vis_name'].strip()
                vis_birth = int(request.POST['vis_birth'])
                vis_sex = request.POST['vis_sex'].strip()
                if any(v.get_name().lower() == vis_name.lower() and v.get_birth_year() == vis_birth for v in tour.get_visitors()):
                    raise ValueError('Такой посетитель уже записан на эту экскурсию')
                tour.add_visitor(Visitor(vis_name, vis_birth, vis_sex))
            elif action == 'remove_visitor_from_tour':
                tour_index = _idx(request.POST['tour_index'], len(zoo.get_tours()), 'Экскурсия')
                vis_index = _idx(request.POST['vis_index'], len(zoo.get_tour(tour_index).get_visitors()), 'Посетитель')
                zoo.get_tour(tour_index).remove_visitor(vis_index)
            _save_zoo(zoo)
            return redirect('tours')
        except Exception as exc:
            error = str(exc)

    tours = zoo.get_tours()
    expositions = zoo.get_expositions()
    guides = zoo.get_guides()

    exp_by_id = {exp.get_id(): exp.get_name() for exp in expositions}
    guide_by_id = {guide.get_id(): guide.get_name() for guide in guides}
    
    # Словари для маппинга порядкового номера (index) экспозиции/гида на их реальный ID
    exp_id_by_index = {i: exp.get_id() for i, exp in enumerate(expositions)}
    guide_id_by_index = {i: guide.get_id() for i, guide in enumerate(guides)}

    context = _base_context(zoo, error)
    context['page'] = 'tours'
    context['tours'] = [
        {
            'index': i,
            'obj': tour,
            'exp_name': exp_by_id.get(tour.get_exposition_id(), f"ID {tour.get_exposition_id()}"),
            'guide_name': guide_by_id.get(tour.get_tour_guide_id(), "Неизвестный экскурсовод"),
        }
        for i, tour in enumerate(tours)
    ]
    context['tour_choices'] = [
        (i, f"{exp_by_id.get(tour.get_exposition_id(), 'Неизвестная экспозиция')} | {tour.get_date().strftime('%d.%m.%Y %H:%M')}")
        for i, tour in enumerate(tours)
    ]
    context['exposition_choices'] = [(i, exp.get_name()) for i, exp in enumerate(expositions)]
    context['guide_choices'] = [(i, f"{guide.get_name()} ({guide.get_languages()})") for i, guide in enumerate(guides)]
    context['tours_with_visitors'] = [
        {
            'tour_index': tour_i,
            'tour_label': f"{exp_by_id.get(tour.get_exposition_id(), 'Экспозиция')} | {tour.get_date().strftime('%d.%m.%Y %H:%M')}",
            'visitors': [{'vis_index': vis_i, 'label': visitor.get_name()} for vis_i, visitor in enumerate(tour.get_visitors())],
        }
        for tour_i, tour in enumerate(tours)
        if tour.get_visitors()
    ]
    
    # ДАННЫЕ ДЛЯ JS: Передаем текущие ID экспозиций и гидов для каждой экскурсии
    context['tour_current_data'] = {
        str(i): {
            'exp_id': tour.get_exposition_id(),
            'guide_id': tour.get_tour_guide_id()
        }
        for i, tour in enumerate(tours)
    }
    # Карты соответствия "Индекс в селекте -> ID сущности"
    context['exp_index_to_id'] = exp_id_by_index
    context['guide_index_to_id'] = guide_id_by_index

    return render(request, 'zoo_web/tours.html', context)


def events_page(request: HttpRequest) -> HttpResponse:
    zoo = _load_zoo()
    error = None

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'add_event':
                name = request.POST['event_name'].strip()
                desc = request.POST['event_desc'].strip()
                max_vis = int(request.POST['event_max'])
                if not name or not desc:
                    raise ValueError('Название и описание мероприятия обязательны')
                if max_vis < 1:
                    raise ValueError('Максимум посетителей должен быть больше 0')
                if any(e.get_name().lower() == name.lower() for e in zoo.get_events()):
                    raise ValueError('Мероприятие с таким названием уже существует')
                zoo.add_event(Event(name, desc, max_vis, [], _parse_dt(request.POST['event_date'])))
            elif action == 'remove_event':
                event_index = _idx(request.POST['event_index'], len(zoo.get_events()), 'Мероприятие')
                zoo.remove_event(event_index)
            elif action == 'change_event_date':
                event_index = _idx(request.POST['event_index'], len(zoo.get_events()), 'Мероприятие')
                event = zoo.get_event(event_index)
                event.change_date(_parse_dt(request.POST['event_date']))
            elif action == 'add_visitor_to_event':
                event_index = _idx(request.POST['event_index'], len(zoo.get_events()), 'Мероприятие')
                event = zoo.get_event(event_index)
                vis_name = request.POST['vis_name'].strip()
                vis_birth = int(request.POST['vis_birth'])
                vis_sex = request.POST['vis_sex'].strip()
                if any(v.get_name().lower() == vis_name.lower() and v.get_birth_year() == vis_birth for v in event.get_visitors()):
                    raise ValueError('Такой посетитель уже записан на это мероприятие')
                event.add_visitor(Visitor(vis_name, vis_birth, vis_sex))
            elif action == 'remove_visitor_from_event':
                event_index = _idx(request.POST['event_index'], len(zoo.get_events()), 'Мероприятие')
                vis_index = _idx(request.POST['vis_index'], len(zoo.get_event(event_index).get_visitors()), 'Посетитель')
                zoo.get_event(event_index).remove_visitor(vis_index)
            _save_zoo(zoo)
            return redirect('events')
        except Exception as exc:
            error = str(exc)

    events = zoo.get_events()
    context = _base_context(zoo, error)
    context['page'] = 'events'
    context['events'] = list(enumerate(events))
    context['event_choices'] = [
        (i, f"{event.get_name()} | {event.get_date().strftime('%d.%m.%Y %H:%M')}")
        for i, event in enumerate(events)
    ]
    context['events_with_visitors'] = [
        {
            'event_index': event_i,
            'event_label': f"{event.get_name()} | {event.get_date().strftime('%d.%m.%Y %H:%M')}",
            'visitors': [{'vis_index': vis_i, 'label': visitor.get_name()} for vis_i, visitor in enumerate(event.get_visitors())],
        }
        for event_i, event in enumerate(events)
        if event.get_visitors()
    ]
    return render(request, 'zoo_web/events.html', context)


def enclosure_detail_page(request: HttpRequest, enc_index: int) -> HttpResponse:
    zoo = _load_zoo()
    error = None
    try:
        enc_index = _idx(str(enc_index), len(zoo.get_enclosures()), 'Вольер')
        enclosure = zoo.get_enclosure(enc_index)
    except Exception:
        return redirect('enclosures')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'add_animal':
                name = request.POST['animal_name'].strip()
                animal_type = request.POST['animal_type'].strip()
                if not name or not animal_type:
                    raise ValueError('Имя и вид животного обязательны')
                if any(a.get_name().lower() == name.lower() for a in enclosure.get_animals()):
                    raise ValueError('Животное с таким именем уже есть в вольере')
                enclosure.add_animal(Animal(name, animal_type))
            elif action == 'remove_animal':
                animal_index = _idx(request.POST['animal_index'], len(enclosure.get_animals()), 'Животное')
                enclosure.remove_animal(animal_index)
            elif action == 'feed_enclosure':
                if not enclosure.get_animals():
                    raise ValueError('Нельзя кормить пустой вольер')
                enclosure.feed(Feed(request.POST['food'], _parse_dt(request.POST['feed_date'])))
            elif action == 'clear_feeds':
                if not enclosure.get_feeds():
                    raise ValueError('Журнал кормлений уже пуст')
                enclosure.clear_feeds()
            elif action == 'vet_service':
                animal_index = _idx(request.POST['animal_index'], len(enclosure.get_animals()), 'Животное')
                vet_index = _idx(request.POST['vet_index'], len(zoo.get_vets()), 'Ветеринар')
                animal = enclosure.get_animal(animal_index)
                vet = zoo.get_vet(vet_index)
                VetService(zoo, vet, animal).execute()
            elif action == 'delete_enclosure':
                zoo.remove_enclosure(enc_index)
                _save_zoo(zoo)
                return redirect('enclosures')
            _save_zoo(zoo)
            return redirect('enclosure_detail', enc_index=enc_index)
        except Exception as exc:
            error = str(exc)

    context = _base_context(zoo, error)
    context['page'] = 'enclosures'
    context['enc_index'] = enc_index
    context['enclosure'] = enclosure
    context['animals'] = list(enumerate(enclosure.get_animals()))
    context['feeds'] = list(enumerate(enclosure.get_feeds()))
    context['vet_choices'] = [(i, f"{vet.get_name()} ({vet.get_specialisation()})") for i, vet in enumerate(zoo.get_vets())]
    return render(request, 'zoo_web/enclosure_detail.html', context)


def vet_detail_page(request: HttpRequest, vet_index: int) -> HttpResponse:
    zoo = _load_zoo()
    try:
        vet_index = _idx(str(vet_index), len(zoo.get_vets()), 'Ветеринар')
    except Exception:
        return redirect('staff')
    context = _base_context(zoo, None)
    context['page'] = 'staff'
    context['vet'] = zoo.get_vet(vet_index)
    context['vet_index'] = vet_index
    related_logs = []
    for log in zoo.get_vet_logs():
        if log.get_vet_id() == context['vet'].get_id():
            animal = zoo.get_animal_by_id(log.get_animal_id())
            related_logs.append((log, animal))
    context['related_logs'] = related_logs
    return render(request, 'zoo_web/vet_detail.html', context)


def guide_detail_page(request: HttpRequest, guide_index: int) -> HttpResponse:
    zoo = _load_zoo()
    try:
        guide_index = _idx(str(guide_index), len(zoo.get_guides()), 'Экскурсовод')
    except Exception:
        return redirect('staff')
    guide = zoo.get_guides()[guide_index]
    guide_tours = []
    for i, tour in enumerate(zoo.get_tours()):
        if tour.get_tour_guide_id() == guide.get_id():
            guide_tours.append((i, tour))
    context = _base_context(zoo, None)
    context['page'] = 'staff'
    context['guide'] = guide
    context['guide_index'] = guide_index
    context['guide_tours'] = guide_tours
    return render(request, 'zoo_web/guide_detail.html', context)


def exposition_detail_page(request: HttpRequest, exp_index: int) -> HttpResponse:
    zoo = _load_zoo()
    error = None
    try:
        exp_index = _idx(str(exp_index), len(zoo.get_expositions()), 'Экспозиция')
        exposition = zoo.get_exposition(exp_index)
    except Exception:
        return redirect('expositions')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'add_enclosure':
                enc_index = _idx(request.POST['enc_index'], len(zoo.get_enclosures()), 'Вольер')
                enc = zoo.get_enclosure(enc_index)
                if enc.get_id() in exposition.get_enclosure_ids():
                    raise ValueError('Этот вольер уже добавлен')
                exposition.add_enclosure(enc.get_id())
            elif action == 'remove_enclosure':
                enc_pos = _idx(request.POST['enc_pos'], len(exposition.get_enclosure_ids()), 'Вольер')
                exposition.remove_enclosure(enc_pos)
            elif action == 'delete_exposition':
                zoo.remove_exposition(exposition)
                _save_zoo(zoo)
                return redirect('expositions')
            _save_zoo(zoo)
            return redirect('exposition_detail', exp_index=exp_index)
        except Exception as exc:
            error = str(exc)

    ids = exposition.get_enclosure_ids()
    all_enclosures = zoo.get_enclosures()
    attached = [(i, enc) for i, enc in enumerate(all_enclosures) if enc.get_id() in ids]
    available = [(i, enc) for i, enc in enumerate(all_enclosures) if enc.get_id() not in ids]
    context = _base_context(zoo, error)
    context['page'] = 'expositions'
    context['exp_index'] = exp_index
    context['exposition'] = exposition
    context['attached_enclosures'] = attached
    context['available_enclosures'] = available
    return render(request, 'zoo_web/exposition_detail.html', context)


def tour_detail_page(request: HttpRequest, tour_index: int) -> HttpResponse:
    zoo = _load_zoo()
    error = None
    try:
        tour_index = _idx(str(tour_index), len(zoo.get_tours()), 'Экскурсия')
        tour = zoo.get_tour(tour_index)
    except Exception:
        return redirect('tours')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'change_tour_date':
                tour.change_date(_parse_dt(request.POST['tour_date']))
            elif action == 'change_tour_exposition':
                exp_index = _idx(request.POST['exp_index'], len(zoo.get_expositions()), 'Экспозиция')
                exp = zoo.get_exposition(exp_index)
                tour.change_exposition_id(exp.get_id())
            elif action == 'change_tour_guide':
                guide_index = _idx(request.POST['guide_index'], len(zoo.get_guides()), 'Экскурсовод')
                guide = zoo.get_guides()[guide_index]
                tour.change_tour_guide_id(guide.get_id())
            elif action == 'add_visitor':
                vis_name = request.POST['vis_name'].strip()
                vis_birth = int(request.POST['vis_birth'])
                vis_sex = request.POST['vis_sex'].strip()
                if any(v.get_name().lower() == vis_name.lower() and v.get_birth_year() == vis_birth for v in tour.get_visitors()):
                    raise ValueError('Такой посетитель уже записан')
                tour.add_visitor(Visitor(vis_name, vis_birth, vis_sex))
            elif action == 'remove_visitor':
                vis_index = _idx(request.POST['vis_index'], len(tour.get_visitors()), 'Посетитель')
                tour.remove_visitor(vis_index)
            elif action == 'delete_tour':
                zoo.remove_tour(tour_index)
                _save_zoo(zoo)
                return redirect('tours')
            _save_zoo(zoo)
            return redirect('tour_detail', tour_index=tour_index)
        except Exception as exc:
            error = str(exc)

    exp = zoo.get_exposition_by_id(tour.get_exposition_id())
    guide = zoo.get_guide_by_id(tour.get_tour_guide_id())
    exposition_index = None
    for i, exposition in enumerate(zoo.get_expositions()):
        if exposition.get_id() == tour.get_exposition_id():
            exposition_index = i
            break
    context = _base_context(zoo, error)
    context['page'] = 'tours'
    context['tour_index'] = tour_index
    context['tour'] = tour
    context['tour_exp_name'] = exp.get_name() if exp else 'Неизвестная экспозиция'
    context['tour_guide_name'] = guide.get_name() if guide else 'Неизвестный экскурсовод'
    context['tour_exp_index'] = exposition_index
    context['visitors'] = list(enumerate(tour.get_visitors()))
    context['exposition_choices'] = [
        (i, e.get_name()) 
        for i, e in enumerate(zoo.get_expositions()) 
        if e.get_id() != tour.get_exposition_id()
    ]
    context['guide_choices'] = [
        (i, f'{g.get_name()} ({g.get_languages()})') 
        for i, g in enumerate(zoo.get_guides()) 
        if g.get_id() != tour.get_tour_guide_id()
    ]
    return render(request, 'zoo_web/tour_detail.html', context)


def event_detail_page(request: HttpRequest, event_index: int) -> HttpResponse:
    zoo = _load_zoo()
    error = None
    try:
        event_index = _idx(str(event_index), len(zoo.get_events()), 'Мероприятие')
        event = zoo.get_event(event_index)
    except Exception:
        return redirect('events')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            if action == 'change_event_date':
                event.change_date(_parse_dt(request.POST['event_date']))
            elif action == 'add_visitor':
                vis_name = request.POST['vis_name'].strip()
                vis_birth = int(request.POST['vis_birth'])
                vis_sex = request.POST['vis_sex'].strip()
                if any(v.get_name().lower() == vis_name.lower() and v.get_birth_year() == vis_birth for v in event.get_visitors()):
                    raise ValueError('Такой посетитель уже записан')
                event.add_visitor(Visitor(vis_name, vis_birth, vis_sex))
            elif action == 'remove_visitor':
                vis_index = _idx(request.POST['vis_index'], len(event.get_visitors()), 'Посетитель')
                event.remove_visitor(vis_index)
            elif action == 'delete_event':
                zoo.remove_event(event_index)
                _save_zoo(zoo)
                return redirect('events')
            _save_zoo(zoo)
            return redirect('event_detail', event_index=event_index)
        except Exception as exc:
            error = str(exc)

    context = _base_context(zoo, error)
    context['page'] = 'events'
    context['event_index'] = event_index
    context['event'] = event
    context['visitors'] = list(enumerate(event.get_visitors()))
    return render(request, 'zoo_web/event_detail.html', context)
