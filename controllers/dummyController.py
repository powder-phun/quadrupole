from controllers.controller import Controller

class DummyController(Controller):
    def __init__(self, config):
        self.value: float = 0
        self.config = config

        self.value_name: str = "Dummy 1"
        self.value_name_out: str = "Dummy Out 1"

    @staticmethod
    def getName():
        return "dummy"

    def adjust(self, param: str, value: float) -> None:
        self.value = value

    def connect(self) -> bool:
        return True

    def read(self, param: str) -> float:
        if param == self.value_name:
            return self.value
        elif param == self.value_name_out:
            return self.value * 2