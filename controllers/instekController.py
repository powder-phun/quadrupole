import serial
from serial.tools import list_ports

from controllers.controller import Controller
from parameter import ParameterID, Parameter

class InstekController(Controller):
    def __init__(self):
        self.serial = None
        self.voltage1 = 0
        self.voltage2 = 0

    def getHandled(self):
        return {
            ParameterID.INSTEK_V_1: Parameter(ParameterID.INSTEK_V_1, "Instek V1", "V", True, 0, 32),
            ParameterID.INSTEK_V_2: Parameter(ParameterID.INSTEK_V_2, "Instek V2", "V", True, 0, 32),
        }

    def adjust(self, param: ParameterID, value: float) -> None:
        if param == ParameterID.INSTEK_V_1:
            self.voltage1 = value
            self.serial.write("VSET1:{:.3f}\r\n".format(value).encode("ASCII"))
        if param == ParameterID.INSTEK_V_2:
            self.voltage2 = value
            self.serial.write("VSET2:{:.3f}\r\n".format(value).encode("ASCII"))
            

    def connect(self) -> bool:
        ports = list(list_ports.comports())
        self.serial = serial.Serial()
        self.serial.baudrate = 9600
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 1
        
        print("GW Instek: Connecting")

        for port in ports:
            try:
                print(f"GW Instek: Trying: {port.device}")
                self.serial.port = port.device
                self.serial.open()
                self.serial.write("*IDN?\r\n".encode("ASCII"))
                ret = self.serial.readline()[:20].decode("ASCII")
                if "GPD" in ret:
                    print("GW Instek: Connected")
                    return True
            except Exception as e:
                print(e)
        return False


    def read(self, param: ParameterID) -> float:
        if param == ParameterID.INSTEK_V_1:
            return self.voltage1
        elif param == ParameterID.INSTEK_V_2:
            return self.voltage2

    def enable(self, state: bool):
        if state:
            self.serial.write("OUT1\r\n".encode("ASCII"))
        else:
            self.serial.write("OUT0\r\n".encode("ASCII"))