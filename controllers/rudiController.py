from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils
import numpy as np


from controllers.controller import Controller
from parameter import ParameterID, Parameter

class RudiController(Controller):
    def __init__(self):
        self.device = None
        self.voltage1 = 0
        self.voltage2 = 0
        self.voltage3 = 0
        self.voltage4 = 0

    def getHandled(self):
        return {
            ParameterID.RUDI_1: Parameter(ParameterID.RUDI_1, "RUDI 1", "V", True, 0, 1500),
            ParameterID.RUDI_2: Parameter(ParameterID.RUDI_2, "RUDI 2", "V", True, 0, 1500),
            ParameterID.RUDI_3: Parameter(ParameterID.RUDI_3, "RUDI 3", "V", True, 0, 1500),
            ParameterID.RUDI_4 : Parameter(ParameterID.RUDI_4, "RUDI 4", "V", True, 0, 1500),
        }

    def adjust(self, param: ParameterID, value: float) -> None:
        voltageMilivolts = np.uint32(value * 1000)
        words = utils.long_list_to_word([voltageMilivolts])
        if param == ParameterID.RUDI_1:
            self.device.unit_id = 1
            self.voltage1 = value
        elif param == ParameterID.RUDI_2:
            self.device.unit_id = 2
            self.voltage2 = value
        elif param == ParameterID.RUDI_3:
            self.device.unit_id = 3
            self.voltage3 = value
        elif param == ParameterID.RUDI_4:
            self.device.unit_id = 4
            self.voltage4 = value

        self.device.write_multiple_registers(2, words)

    def connect(self) -> bool:
        self.device = ModbusClient(host="169.254.100.22", port=502, auto_open=True, auto_close=True)
        return True

    def changeMode(self, value):
        self.device.unit_id = 1
        self.device.write_single_register(5, value)
        self.device.unit_id = 2
        self.device.write_single_register(5, value)
        self.device.unit_id = 3
        self.device.write_single_register(5, value)
        self.device.unit_id = 4
        self.device.write_single_register(5, value)

    def enable(self, state: bool):
        if state:
            self.changeMode(5)
        else:
            self.changeMode(7)


    def read(self, param: ParameterID) -> float:
        if param == ParameterID.RUDI_1:
            return self.voltage1
        elif param == ParameterID.RUDI_2:
            return self.voltage2
        elif param == ParameterID.RUDI_3:
            return self.voltage3
        elif param == ParameterID.RUDI_4:
            return self.voltage4