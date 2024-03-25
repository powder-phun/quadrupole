import vxi11
import time
import logging
import pyvisa
import serial
import matplotlib.pyplot as plt
import numpy as np

from controllers.controller import Controller
from config import ParamConfig
from config import ControllerConfig
from time import sleep
from device import Device


class HamegHM5014Controller(Controller):
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
        return "HM5014"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "Amax": False,
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "Amax": "dB"
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}

    def parseConfig(self):
        if "port" in self.config.json:
            self.serial_port = self.config.json["port"]
        else:
            logging.error("No port specified")
            return False

        self.param = self.config.params[0].name

        if "center_freq" in self.config.json:
            self.center_freq = float(self.config.json["center_freq"])
        else:
            self.center_freq = None
        
        if "span" in self.config.json:
            self.span = self.config.json["span"]
        else:
            self.span = None

        if "config_commands" in self.config.json:
            self.config_commands = self.config.json["config_commands"]
        else:
            self.config_commands = None

        return True

    def adjust(self, param: str, value: float) -> None:
        logging.error("No adjustable params")

    def connect(self) -> bool:
        self.ser = serial.Serial(self.serial_port, 4800)
        self.ser.write(b'#kl1\r')
        self.ser.write(b'#br115200\r')
        self.ser.close()
        time.sleep(1)
        self.ser = serial.Serial(self.serial_port, 115200)

        self.ser.write(b'#kl1\r')

        if self.center_freq is not None:
            self.ser.write("#cf{:08.3f}\r".format(self.center_freq).encode())
            print("#cf{:08.3f}\r".format(self.center_freq).encode())
        if self.span is not None:
            self.ser.write((f"#cf{self.span}\r").encode())
        if self.config_commands is not None:
            self.ser.write(self.config_commands.encode())
        print("sent")
        return True


    def enable(self, state: bool):
        print("enable")
        pass


    def read(self, param: str) -> float:
        print("read")
        if param == "Amax":
            self.ser.flushInput()
            self.ser.write((f"#bm1\r").encode())
            c = self.ser.read(5)
            c = self.ser.read(2001)

            print(c)
            np_array = np.frombuffer(c, dtype=np.uint8)
            #plt.plot(np_array)
            #plt.show()

            print(self.ser.in_waiting)
            return(np.max(np_array))
        else:
            logging.error("Wrong param name")
