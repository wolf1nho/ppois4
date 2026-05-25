class IDGenerator:
    _instance = None
    _counter = 0

    def __new__(cls, start=0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._counter = start
        return cls._instance
    
    def generate(self) -> int:
        IDGenerator._counter += 1
        return IDGenerator._counter
    
    def get_counter(self):
        return self._counter