import serial
import logging
from euromeasure import EuroMeasure


from config import ControllerConfig, ParamConfig
from controllers.controller import Controller

import vxi11
import pyvisa

from controllers.controller import Controller
import time
from device import Device



class Scanner_channel():
    def __init__(self, param, device, scanner_device):
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

        if "averaging_time" in param.json:
            self.averaging = True
            self.avg_time = self.config.json["averaging_time"]
        else:
            self.averaging = False
        
        if "int_nplc" in param.json:
            self.nplc = self.config.json["int_nplc"]
        else:
            self.nplc = "default"
        
        if "range" in param.json:
            self.range = self.config.json["range"]
        else:
            self.range = ""
    


    def read(self):
        self.device.write(f"CONF:{self.type} {str(self.range)}")
        self.device.write(f"trigger:source immediate")
        if self.averaging:
            pass
        else:
            self.device.write(f"trigger:count 1")
        self.device.write(f"sense:{self.type}:nplc {str(self.nplc)}")

        time.sleep(0.1)

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

    



    isEditable = None
    unit = ""
    min = float('-inf')
    max = float('inf')
    n_channels = None
    state = None

class HP34401AScannerController(Controller):
    def __init__(self, config):
        self.config: ControllerConfig = config

        self.device = None
        self.ip = None
        self.usb = None
        self.serial_port = None

        self.parseConfig()

    @staticmethod
    def getName():
        return "HP34401AScanner"

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
        
        if "scanner_port" in self.config.json:
            self.scanner_port = self.config.json["scanner_port"]
        else:
            logging.error("No port for scanner specified")

        
        for param in self.config.params:
            self.params[param.name] = Scanner_channel(param.json)
        return True
    
    def connect(self) -> bool:
        self.device = Device(usb=self.usb, ip=self.ip, serial_port=self.serial_port)
        ret = self.device.connect()
        self.device.write(f"trigger:source immediate")


        self.scanner_device = Device(serial_port=self.scanner_port)
        ret2 = self.scanner_device.connect()
        return ret and ret2

    def adjust(self, param: str, value: float) -> None:
        logging.error("No adjustable params")

    def enable(self, state: bool):
        pass

    def read(self, param: str) -> float:
        return(self.params[param].read())