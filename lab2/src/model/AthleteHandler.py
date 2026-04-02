import xml.sax
from src.model.Athlete import Athlete

class AthleteHandler(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.athletes: list[Athlete] = []
        self.current_data = ""
        self.p_data = {}

    def startElement(self, tag, attrs):
        self.current_data = tag

    def characters(self, content):
        if content.strip():
            self.p_data[self.current_data] = content.strip()

    def endElement(self, tag):
        if tag == "athlete":
            self.athletes.append(Athlete(**self.p_data))
            self.p_data = {}