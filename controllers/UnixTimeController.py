import time
import logging

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig
import time
from device import Device


class UnixTimeController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.usb = None
        self.serial_port = None
        self.param = None
        self.type = None

        self.parseConfig()

    @staticmethod
    def getName():
        return "UnixTime"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "time": False,
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "time": "s"
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}

    def parseConfig(self):
        self.param = self.config.params[0].name
        return True

    def adjust(self, param: str, value: float) -> None:
        logging.error("No adjustable params")

    def connect(self) -> bool:
        return True


    def enable(self, state: bool):
        pass


    def read(self, param: str) -> float:
        if param == "time":
            return(float(time.time()))
        else:
            logging.error("Wrong param name")
