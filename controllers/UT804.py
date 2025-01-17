import serial

from controllers.controller import Controller

class UT804Controller(Controller):
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
        return "ut804"

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

    def read(self, param: str) -> float:
        if param == self.name:
            self.serial.reset_input_buffer()
            data = self.serial.readline().decode("ASCII")
            try:
                decimal_position = int(data[5])
                value = float(data[0:decimal_position] + "." + data[decimal_position:5])
            except ValueError:
                value = float('nan')
            except IndexError:
                value = 0.0
            return value
            


    def adjust(self, param: str, value: float) -> None:
        pass

    def connect(self) -> bool:
        self.serial = serial.Serial()
        self.serial.baudrate = 2400
        self.serial.bytesize = serial.SEVENBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = None
        self.serial.dtr = True
        self.serial.port = self.port
        self.serial.open()
        return True
