import json
import os

from src.Enclosure import Enclosure
from src.Vet import Vet
from src.VetLog import VetLog
from src.TourGuide import TourGuide
from src.Exposition import Exposition
from src.Tour import Tour
from src.Event import Event
from src.Zoo import Zoo


class ZooDataManager:
    def __init__(self, file_path: str = "zoo.json") -> None:
        self._file_path = file_path

    def save(self, zoo: Zoo) -> None:
        data = {
            "name": zoo.get_name(),
            "enclosures": [enc.to_dict() for enc in zoo.get_enclosures()],
            "vets": [m.to_dict() for m in zoo.get_vets()],
            "vet logs": [vl.to_dict() for vl in zoo.get_vet_logs()],
            "guides": [g.to_dict() for g in zoo.get_guides()],
            "expositions": [exp.to_dict() for exp in zoo.get_expositions()],
            "tours": [t.to_dict() for t in zoo.get_tours()],
            "events":[ev.to_dict() for ev in zoo.get_events()],
            "id counter": zoo.get_id_counter()
        }
        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load(self) -> Zoo:
        if not os.path.exists(self._file_path):
            return Zoo()

        with open(self._file_path, 'r', encoding='utf-8') as f:
            data: dict = json.load(f)

        zoo = Zoo(data["name"], data["id counter"])

        enc_data: dict
        for enc_data in data.get("enclosures", []):
            zoo.add_enclosure(Enclosure.from_dict(enc_data))

        v_data: dict
        for v_data in data.get("vets", []):
            zoo.add_vet(Vet.from_dict(v_data))

        vl_data: dict
        for vl_data in data.get("vet logs", []):
            zoo.add_vet_log(VetLog.from_dict(vl_data))

        g_data: dict
        for g_data in data.get("guides", []):
            zoo.add_guide(TourGuide.from_dict(g_data))  
        
        exp_data: dict
        for exp_data in data.get("expositions", []):
            zoo.add_exposition(Exposition.from_dict(exp_data))

        t_data: dict
        for t_data in data.get("tours", []):
            zoo.add_tour(Tour.from_dict(t_data))

        e_data: dict
        for e_data in data.get("events", []):
            zoo.add_event(Event.from_dict(e_data))

        return zoo