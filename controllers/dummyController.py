from controllers.controller import Controller
from config import ParamConfig
import logging

class DummyController(Controller):
    def __init__(self, config):
        self.value: float = 0
        self.config = config

        self.value_name: str = None
        self.value_name_out: str = None

        self.parseConfig()

    def parseConfig(self):
        for param in self.config.params:
            if param.type == "dummy":
                self.value_name = param.name
            elif param.type == "dummy_out":
                self.value_name_out = param.name

    @staticmethod
    def getName():
        return "dummy"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "dummy": True,
            "dummy_out": False
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "dummy": "-",
            "dummy_out": "-"
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}


    def adjust(self, param: str, value: float) -> None:
        self.value = value

    def connect(self) -> bool:
        return True

    def read(self, param: str) -> float:
        if param == self.value_name:
            return self.value
        elif param == self.value_name_out:
            return self.value * 2