from controllers.controller import Controller

from parameter import Parameter

class DummyController(Controller):
    def __init__(self, config):
        self.value: float = 0
        self.config = config

        self.value_name: str = None
        self.value_name_out: str = None

        self.params: dict(str, Parameter) = {}

        self.parseConfig()

    def parseConfig(self):
        for param in self.config.params:
            if param.type == "dummy":
                self.value_name = param.name
                self.params[param.name] = Parameter(param.name, "-", True, -1e99, 1e99)
            elif param.type == "dummy_out":
                self.value_name_out = param.name
                self.params[param.name] = Parameter(param.name, "-", False, -1e99, 1e99)

    @staticmethod
    def getName():
        return "dummy"

    def getHandled(self) -> dict:
        return self.params

    def adjust(self, param: str, value: float) -> None:
        self.value = value

    def connect(self) -> bool:
        return True

    def read(self, param: str) -> float:
        if param == self.value_name:
            return self.value
        elif param == self.value_name_out:
            return self.value * 2