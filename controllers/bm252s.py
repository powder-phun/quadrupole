import serial

from controllers.controller import Controller
import logging


class BM252sController(Controller):
    def __init__(self, config):
        self.serial = None
        self.port = None
        self.name: str | None = None
        self.config = config
        self.parseConfig()

    def parseConfig(self):
        for param in self.config.params:
            if param.type == "value":
                self.name = param.name
        self.port = self.config.json["port"]

    @staticmethod
    def getName():
        return "bm252s"

    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        return {
            "value": False,
        }

    @staticmethod
    def getUnitDict() -> dict[str, str]:
        return {
            "value": "-",
        }

    @staticmethod
    def getMinDict() -> dict[str, bool]:
        return {}

    @staticmethod
    def getMaxDict() -> dict[str, bool]:
        return {}

    CODE_TO_DIGIT = {
        # afepbgcd
        0b11101011: "0",
        0b00001010: "1",
        0b10101101: "2",
        0b10001111: "3",
        0b01001110: "4",
        0b11000111: "5",
        0b11100111: "6",
        0b10001010: "7",
        0b11101111: "8",
        0b11001111: "9",
    }

    def read_number(self) -> str:
        first = self.serial.read(1)[0]
        second = self.serial.read(1)[0]
        print(bin(first), bin(second))
        b = ((first << 4) & 0b11110000) | (second & 0b00001111)
        print(bin(b))
        point = (b & 0b00010000) > 0
        b = b & 0b11101111
        if b in self.CODE_TO_DIGIT:
            ret = self.CODE_TO_DIGIT[b]
        else:
            ret = ""
            logging.error(f"Invalid digit code: {bin(b)}")
        # if point:
        #    ret += "."
        return ret

    def read(self, param: str) -> float:
        if param == self.name and self.serial is not None:
            self.serial.reset_input_buffer()
            b = self.serial.read(1)[0]
            while b != 0b00000010:
                b = self.serial.read(1)[0]
            b = self.serial.read(1)[0]  # symbols row 2
            b = self.serial.read(1)[0]  # symbols row 3
            value = self.read_number()
            value += self.read_number()
            value += self.read_number()
            value += self.read_number()
            b = self.serial.read(1)[0]  # symbols row 12
            b = self.serial.read(1)[0]  # symbols row 13
            b = self.serial.read(1)[0]  # symbols row 14
            b = self.serial.read(1)[0]  # symbols row 15
            return float(value)

    def adjust(self, param: str, value: float) -> None:
        pass

    def connect(self) -> bool:
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = None
        self.serial.dtr = True
        self.serial.port = self.port
        self.serial.open()
        return True
