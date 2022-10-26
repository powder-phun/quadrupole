import vxi11
import time
import logging

from controllers.controller import Controller
from parameter import Parameter
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

    def parseConfig(self):
        if "ip" in self.config.json:
            self.ip = self.config.json["ip"]
        else:
            logging.error("No ip address specified")
            return False

        for param in self.config.params: 
            if param.type == "currentOne":
                self.currentOneParam = Parameter(param.name, "I", True, -9e99, 9e99)
            elif param.type == "voltageOne":
                self.voltageOneParam = Parameter(param.name, "V", True, -9e99, 9e99)
            elif param.type == "currentTwo":
                self.currentTwoParam = Parameter(param.name, "I", True, -9e99, 9e99)
            elif param.type == "voltageTwo":
                self.voltageTwoParam = Parameter(param.name, "V", True, -9e99, 9e99)
            else:
                logging.error(f"Invalid parameter name {param}")

        return True

    def getHandled(self):
        handled = {}
        if self.voltageOneParam is not None:
            handled[self.voltageOneParam.name] = self.voltageOneParam
        if self.currentOneParam is not None:
            handled[self.currentOneParam.name] = self.currentOneParam
        if self.voltageTwoParam is not None:
            handled[self.voltageTwoParam.name] = self.voltageTwoParam
        if self.currentTwoParam is not None:
            handled[self.currentTwoParam.name] = self.currentTwoParam
        return handled

    def adjust(self, param: str, value: float) -> None:
        if param == self.currentOneParam.name:
            self.device.write(f"CH1:CURR {value:.3f}")
        elif param == self.voltageOneParam.name:
            self.device.write(f"CH1:VOLT {value:.3f}")
        elif param == self.currentTwoParam.name:
            self.device.write(f"CH2:CURR {value:.3f}")
        elif param == self.voltageTwoParam.name:
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
        if param == self.currentOneParam.name:
            return float(self.device.ask(f"MEAS:CURR? CH1"))
        elif param == self.voltageOneParam.name:
            return float(self.device.ask(f"MEAS:VOLT? CH1"))
        elif param == self.currentTwoParam.name:
            return float(self.device.ask(f"MEAS:CURR? CH2"))
        elif param == self.voltageTwoParam.name:
            return float(self.device.ask(f"MEAS:VOLT? CH2"))
        else:
            logging.error("Wrong param name")
