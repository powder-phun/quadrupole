import vxi11
import time
import logging

from controllers.controller import Controller
from parameter import Parameter
from config import ControllerConfig

class SDMController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.param = None
        self.type = None

        ret = self.parseConfig()
        if ret is None:
            return None
    
    @staticmethod
    def getName():
        return "sdm"

    def parseConfig(self):
        if "ip" in self.config.json:
            self.ip = self.config.json["ip"]
        else:
            logging.error("No ip address specified")
            return False

        for param in self.config.params: 
            if param.type == "VDC":
                self.param = Parameter(param.name, "V", False, -9e99, 9e99)
                self.type = "VOLT:DC"
            elif param.type == "VAC":
                self.param = Parameter(param.name, "V", False, -9e99, 9e99)
                self.type = "VOLT:AC"
            elif param.type == "RES":
                self.param = Parameter(param.name, "Ω", False, -9e99, 9e99)
                self.type = "RES"
            elif param.type == "IDC":
                self.param = Parameter(param.name, "A", False, -9e99, 9e99)
                self.type = "CURR:DC"
            elif param.type == "IAC":
                self.param = Parameter(param.name, "A", False, -9e99, 9e99)
                self.type = "CURR:AC"
            else:
                logging.error(f"Invalid parameter name {param}")

        return True

    def getHandled(self):
        handled = {}
        if self.param is not None:
            handled[self.param.name] = self.param
        return handled

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
        if param == self.param.name:
            return float(self.device.ask(f"MEAS:{self.type}?"))
        else:
            logging.error("Wrong param name")
