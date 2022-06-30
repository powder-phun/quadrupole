import serial
from serial.tools import list_ports

from controllers.controller import Controller
from parameter import ParameterID, Parameter

class PressureController(Controller):
    def __init__(self):
        self.serial = None

    def getHandled(self):
        return {
            ParameterID.PRESSURE: Parameter(ParameterID.PRESSURE, "Pressure", "mbar", True, 0, 1e3),
        }

    def adjust(self, param: ParameterID, value: float) -> None:
        if param == ParameterID.PRESSURE:
            if value > 2e-2:
                value = 2e-2
            self.serial.write("PRS={:.2E}\r\n".format(value).encode("ASCII"))
            

    def connect(self) -> bool:
        ports = list(list_ports.comports())
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 1

        for port in ports:
            try:
                print(port.device)
                self.serial.port = port.device
                self.serial.open()
                self.serial.write("VER?\r\n".encode("ASCII"))
                ret = self.serial.readline().decode("ASCII")
                if "VER" in ret:
                    return True
            except Exception as e:
                print(e)
        return False


    def read(self, param: ParameterID) -> float:
        if param == ParameterID.PRESSURE:
            self.serial.write("PRI?\r\n".encode("ASCII"))
            ret = self.serial.readline().decode("ASCII")
            ret = float(ret.split(" ")[1][:-6])
            return ret