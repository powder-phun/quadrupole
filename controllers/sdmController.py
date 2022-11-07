import vxi11
import time
import logging

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig

class SDMController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.param = None
        self.type = None

        self.parseConfig()

    @staticmethod
    def getName():
        return "sdm"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "VDC": False,
            "VAC": False,
            "RES": False,
            "IDC": False,
            "IAC": False
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "VDC": "V",
            "VAC": "Vrms",
            "RES": "Ohm",
            "IDC": "A",
            "IAC": "Arms"
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}

    def parseConfig(self):
        if "ip" in self.config.json:
            self.ip = self.config.json["ip"]
        else:
            logging.error("No ip address specified")
            return False

        for param in self.config.params: 
            if param.type == "VDC":
                self.type = "VOLT:DC"
            elif param.type == "VAC":
                self.type = "VOLT:AC"
            elif param.type == "RES":
                self.type = "RES"
            elif param.type == "IDC":
                self.type = "CURR:DC"
            elif param.type == "IAC":
                self.type = "CURR:AC"
            else:
                logging.error(f"Invalid parameter name {param}")

        self.param = self.config.params[0].name

        return True

    def adjust(self, param: str, value: float) -> None:
        logging.error("No adjustable params")

    def connect(self) -> bool:
        if self.device is None:
            if self.ip is not None:
                try:
                    self.device = vxi11.Instrument(self.ip)
                    return True
                except:
                    logging.error(f"Couldn't connect to {self.ip}")
                    return False
            else:
                logging.error(f"No ip is set")
                return False
        else:
            return True


    def enable(self, state: bool):
        pass


    def read(self, param: str) -> float:
        if param == self.param:
            ret = self.device.ask(f"MEAS:{self.type}?")
            print(ret)
            return float(ret)
        else:
            print(self.param)
            logging.error("Wrong param name")
