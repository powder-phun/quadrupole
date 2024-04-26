import vxi11
import time
import logging
import pyvisa

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig
from time import sleep
from device import Device

class HP34401AController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.usb = None
        self.serial_port = None
        self.params = {}
        self.type = None

        self.parseConfig()

    @staticmethod
    def getName():
        return "HP34401A"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "VDC": False,
            "VAC": False,
            "RES": False,
            "IDC": False,
            "IAC": False,
            "FREQ": False,
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "VDC": "V",
            "VAC": "Vrms",
            "RES": "Ohm",
            "IDC": "A",
            "IAC": "Arms",
            "FREQ": "Hz"
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
        elif "usb" in self.config.json:
            self.usb = self.config.json["usb"]
        elif "port" in self.config.json:
            self.serial_port = self.config.json["port"]
        else:
            logging.error("No ip address or usb specified")
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
            elif param.type == "FREQ":
                self.type = "FREQ"
            elif param.type == "TEMP":
                self.type = "TEMP RTD,PT100"
            else:
                logging.error(f"Invalid parameter name {param}")

        self.param = self.config.params[0].name

        if "averaging_time" in self.config.json:
            self.averaging = True
            self.avg_time = self.config.json["averaging_time"]
        else:
            self.averaging = False
        
        if "int_nplc" in self.config.json:
            self.nplc = self.config.json["int_nplc"]
        else:
            self.nplc = "default"
        
        if "range" in self.config.json:
            self.range = self.config.json["range"]
        else:
            self.range = ""


        return True

    def adjust(self, param: str, value: float) -> None:
        logging.error("No adjustable params")

    def connect(self) -> bool:
        self.device = Device(usb=self.usb, ip=self.ip, serial_port=self.serial_port)
        ret = self.device.connect()
        self.device.write(f"CONF:{self.type} {str(self.range)}")
        self.device.write(f"trigger:source immediate")
        if self.averaging:
            pass
        else:
            self.device.write(f"trigger:count 1")
        #self.device.write(f"trigger:delay 0")
        self.device.write(f"sense:{self.type}:nplc {str(self.nplc)}")
        self.device.write(f"initiate")
        return ret


    def enable(self, state: bool):
        pass


    def read(self, param: str) -> float:
        if param == self.param:
            if self.averaging:
                
                self.device.write(f"SAMP:COUN 1000")
                self.device.write(f"CALC:AVER:stat 1")
                self.device.write(f"init")
                time.sleep(float(self.avg_time))
                ret = self.device.ask(f"calc:aver:aver?")
                self.device.write(f"abort")
            else:
                ret = self.device.ask(f"READ?")
            return float(ret)
        else:
            logging.error("Wrong param name")
