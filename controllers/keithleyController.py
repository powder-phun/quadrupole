import pyvisa
import time
import logging

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig

class KeithleyController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.is_cc = False

        self.current = 0
        self.voltage = 0

        self.currentParam = None
        self.voltageParam = None

        ret = self.parseConfig()
        if ret is None:
            return None
    
    @staticmethod
    def getName():
        return "keithley"

    def getIsEditableDict(self) -> dict[str, bool]:
        if self.is_cc:
            return {
                "current": True,
                "voltage": False,
            }
        else:
            return {
                "current": False,
                "voltage": True,
            }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "current": "A",
            "voltage": "V",
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}



    def parseConfig(self):
        if "is_cc" in self.config.json:
            self.is_cc = self.config.json["is_cc"]
        else:
            logging.error('No "is_cc" parameter in keithley config')
            return None

        for param in self.config.params: 
            if param.type == "current":
                self.currentParam = param.name
            elif param.type == "voltage":
                self.voltageParam = param.name

    def adjust(self, param: str, value: float) -> None:
        if param == self.currentParam and self.is_cc:
            self.current = value
            self.device.write("B{:.2E},0,0X".format(value))
            self.device.write("H0X")
        elif param == self.voltageParam and not self.is_cc:
            self.voltage = value
            self.device.write("B{:.2E},0,0X".format(value))
            self.device.write("H0X")
        else:
            logging.error("Wrong param name")


    def connect(self) -> bool:
        if self.device is None:
            rm = pyvisa.ResourceManager()
            devices = rm.list_resources()
            for device in devices:
                if "GPIB" in device:
                    logging.info(f"Connecting to {device}")
                    try:
                        self.device = rm.open_resource(device)

                        self.device.write("J0X") # Restore default settings
                        self.device.write("N0X")  #Standby mode
                        self.device.write("G4,2,0X") # Setup communication format
                        self.device.write("S3") # Linecycle integration

                        if self.is_cc:
                            self.device.write("F1,0X") # Setup DC I Bias
                            self.device.write("L1100,0X") # Setup auto range
                        else:
                            self.device.write("F0,0X") # Setup DC V Bias
                            self.device.write("L1,0X") # Setup auto range

                        return True
                    except:
                        return False
            else:
                return False
        else:
            return True


    def enable(self, state: bool):
        if state:
            self.device.write("N1X")
            self.device.write("H0X")
        else:
            self.device.write("N0X")
            self.device.write("H0X")


    def read(self, param: str) -> float:
        if param == self.voltageParam and self.is_cc:
            val = float(self.device.read().strip())
            return val
        elif param == self.voltageParam and not self.is_cc:
            return self.voltage

        elif param == self.currentParam and self.is_cc:
            return self.current
        elif param == self.currentParam and not self.is_cc:
            val = float(self.device.read().strip())
            return val