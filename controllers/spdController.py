import vxi11
import time
import logging

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig

from device import Device

class SPDController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device: Device = None

        self.currentParam = [None, None]
        self.voltageParam = [None, None]

        self.ip = None
        self.usb = None

        ret = self.parseConfig()
        if ret is None:
            return None
    
    @staticmethod
    def getName():
        return "spd"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "current": True,
            "voltage": True
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "current": "A",
            "voltage": "V"
        }

    @staticmethod
    def getMinDict() -> dict[str, float]:
        return {
            "current": 0,
            "voltage": 0
        }

    @staticmethod
    def getMaxDict() -> dict[str, float]:
        return {
            "current": 3.2,
            "voltage": 32
        }


    def parseConfig(self):
        if "ip" in self.config.json:
            self.ip = self.config.json["ip"]
        elif "usb" in self.config.json:
            self.usb = self.config.json["usb"]
        else:
            logging.error("No ip address or usb specified")
            return False

        for param in self.config.params:
            if param.json.get("channel", 0) == 1 or param.json.get("channel", 0) == 2:
                if param.type == "current":
                    self.currentParam[param.json["channel"]-1] = param.name
                elif param.type == "voltage":
                    self.voltageParam[param.json["channel"]-1] = param.name
                else:
                    logging.error(f"Invalid parameter type {param.type}")
            else:
                logging.error(f"Not specified or invalid channel (should be 1 or 2) for param {param.name}")

        return True

    def adjust(self, param: str, value: float) -> None:
        if param == self.currentParam[0]:
            self.device.write(f"CH1:CURR {value:.3f}")
        elif param == self.voltageParam[0]:
            self.device.write(f"CH1:VOLT {value:.3f}")
        elif param == self.currentParam[1]:
            self.device.write(f"CH2:CURR {value:.3f}")
        elif param == self.voltageParam[1]:
            self.device.write(f"CH2:VOLT {value:.3f}")
        else:
            logging.error("Wrong param name")


    def connect(self) -> bool:
        self.device = Device(usb=self.usb, ip=self.ip)
        ret = self.device.connect()
        return ret



    def enable(self, state: bool):
        self.device.write(f"OUTP CH1,{'ON' if state else 'OFF'}")
        self.device.write(f"OUTP CH2,{'ON' if state else 'OFF'}")


    def read(self, param: str) -> float:
        if param == self.currentParam[0]:
            return float(self.device.ask(f"MEAS:CURR? CH1"))
        elif param == self.voltageParam[0]:
            return float(self.device.ask(f"MEAS:VOLT? CH1"))
        elif param == self.currentParam[1]:
            return float(self.device.ask(f"MEAS:CURR? CH2"))
        elif param == self.voltageParam[1]:
            return float(self.device.ask(f"MEAS:VOLT? CH2"))
        else:
            logging.error("Wrong param name")
