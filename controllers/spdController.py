import vxi11
import time
import logging

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig

class SPDController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None

        self.currentOneParam = None
        self.voltageOneParam = None
        self.currentTwoParam = None
        self.voltageTwoParam = None

        self.ip = None

        ret = self.parseConfig()
        if ret is None:
            return None
    
    @staticmethod
    def getName():
        return "spd"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "currentOne": True,
            "voltageTwo": True,
            "currentOne": True,
            "voltageTwo": True
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "currentOne": "A",
            "voltageTwo": "V",
            "currentOne": "A",
            "voltageTwo": "V"
        }


    def parseConfig(self):
        if "ip" in self.config.json:
            self.ip = self.config.json["ip"]
        else:
            logging.error("No ip address specified")
            return False

        for param in self.config.params: 
            if param.type == "currentOne":
                self.currentOneParam = param.name
            elif param.type == "voltageOne":
                self.voltageOneParam = param.name
            elif param.type == "currentTwo":
                self.currentTwoParam = param.name
            elif param.type == "voltageTwo":
                self.voltageTwoParam = param.name
            else:
                logging.error(f"Invalid parameter name {param}")

        return True

    def adjust(self, param: str, value: float) -> None:
        if param == self.currentOneParam:
            self.device.write(f"CH1:CURR {value:.3f}")
        elif param == self.voltageOneParam:
            self.device.write(f"CH1:VOLT {value:.3f}")
        elif param == self.currentTwoParam:
            self.device.write(f"CH2:CURR {value:.3f}")
        elif param == self.voltageTwoParam:
            self.device.write(f"CH2:VOLT {value:.3f}")
        else:
            logging.error("Wrong param name")


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
        self.device.write(f"OUTP CH1,{'ON' if state else 'OFF'}")
        self.device.write(f"OUTP CH2,{'ON' if state else 'OFF'}")


    def read(self, param: str) -> float:
        if param == self.currentOneParam:
            return float(self.device.ask(f"MEAS:CURR? CH1"))
        elif param == self.voltageOneParam:
            return float(self.device.ask(f"MEAS:VOLT? CH1"))
        elif param == self.currentTwoParam:
            return float(self.device.ask(f"MEAS:CURR? CH2"))
        elif param == self.voltageTwoParam:
            return float(self.device.ask(f"MEAS:VOLT? CH2"))
        else:
            logging.error("Wrong param name")
