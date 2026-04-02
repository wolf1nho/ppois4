from src.model.Athlete import Athlete
import xml.sax
import xml.dom.minidom
from src.model.AthleteHandler import AthleteHandler

class AthleteModel:
    def __init__(self):
        self.notes: list[Athlete] = []

    def get_data(self) -> list[Athlete]:
        return self.notes

    def add(self, athlete):
        self.notes.append(athlete)

    def handle_import(self, file_path):
        handler = AthleteHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(file_path)
        self.notes = handler.athletes
    
    def handle_export(self, file_path):
        athletes = self.notes

        doc = xml.dom.minidom.Document()

        root_element = doc.createElement('athletes')
        doc.appendChild(root_element)

        def add_text_node(parent, tag_name, value):
            child = doc.createElement(tag_name)
            text = doc.createTextNode(str(value))
            child.appendChild(text)
            parent.appendChild(child)

        for athlete in athletes:
            athlete_node = doc.createElement('athlete')
            root_element.appendChild(athlete_node)

            add_text_node(athlete_node, 'name', athlete.name)
            add_text_node(athlete_node, 'sport', athlete.sport)
            add_text_node(athlete_node, 'position', athlete.position)
            add_text_node(athlete_node, 'team', athlete.team)
            add_text_node(athlete_node, 'titles', athlete.titles)
            add_text_node(athlete_node, 'rank', athlete.rank)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(doc.toprettyxml(indent="  "))

    def search(self, search_params) -> list[Athlete]:
        filtered_athletes = []
        name = search_params["name"].lower()
        sport = search_params["sport"].lower()
        min_t = search_params["min_titles"]
        max_t = search_params["max_titles"]
        rank = search_params["rank"]
        for athlete in self.notes:
            match_name = name in athlete.name.lower()
            match_sport = sport in athlete.sport.lower()
            
            nums = ''.join(filter(str.isdigit, athlete.titles))
            count = int(nums) if nums else 0
            match_titles = min_t <= count <= max_t
            
            match_rank = (rank == "Любой" or rank == athlete.rank)

            if match_name and match_sport and match_titles and match_rank:
                filtered_athletes.append(athlete)
        return filtered_athletes

    def delete(self, athlete):
        self.notes.remove(athlete)

    def delete_searched(self, search_params) -> int:
        deleted_notes = 0
        name = search_params["name"].lower()
        sport = search_params["sport"].lower()
        min_t = search_params["min_titles"]
        max_t = search_params["max_titles"]
        rank = search_params["rank"]
        for i in range(len(self.notes) - 1, -1, -1):
            athlete = self.notes[i]

            match_name = name in athlete.name.lower()
            match_sport = sport in athlete.sport.lower()

            nums = ''.join(filter(str.isdigit, athlete.titles))
            count = int(nums) if nums else 0
            match_titles = min_t <= count <= max_t

            match_rank = (rank == "Любой" or rank == athlete.rank)

            if match_name and match_sport and match_titles and match_rank:
                self.notes.pop(i)
                deleted_notes += 1

        return deleted_notes
