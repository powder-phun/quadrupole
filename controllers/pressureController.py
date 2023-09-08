import serial
from serial.tools import list_ports

from controllers.controller import Controller

class PressureController(Controller):
    def __init__(self, config):
        self.serial = None
        self.port = None
        self.name: str = None
        self.config = config
        self.parseConfig()

    def parseConfig(self):
        for param in self.config.params:
            if param.type == "pressure":
                self.name = param.name
        self.port = self.config.json["port"]

    @staticmethod
    def getName():
        return "pressure"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "pressure": False,
        }
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "pressure": "mbar",
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}

    def read(self, param: str) -> float:
        if param == self.name:
            print(f"Reading from pressure gauge. {self.port} {self.name}")
            self.serial.write("PRI?\r\n".encode("ASCII"))
            ret = self.serial.readline().decode("ASCII")
            print(ret)
            if ">" in ret:
                ret = float(ret.split(">")[1][:-6])
            else:
                ret = float(ret.split(" ")[1][:-6])
            return ret

    def adjust(self, param: str, value: float) -> None:
        if param == self.name:
            if value > 2e-2:
                value = 2e-2
            self.serial.write("PRS={:.2E}\r\n".format(value).encode("ASCII"))
            

    def connect(self) -> bool:
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 1
        self.serial.port = self.port
        self.serial.open()
        return True