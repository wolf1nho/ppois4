class EnclosureError(Exception):
    def __init__(self, msg: str = "Ошибка при работе с вольерами") -> None:
        super().__init__(msg)
        self.msg: str = msg

class ExpositionError(Exception):
    def __init__(self, msg: str = "Ошибка при работе с экспозициями") -> None:
        super().__init__(msg)
        self.msg: str = msg

class TourError(Exception):
    def __init__(self, msg: str = "Ошибка при работе с экскурсиями") -> None:
        super().__init__(msg)
        self.msg: str = msg

class EventError(Exception):
    def __init__(self, msg: str = "Ошибка при работе с мероприятиями") -> None:
        super().__init__(msg)
        self.msg: str = msg