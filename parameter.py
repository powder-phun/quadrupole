from enum import Enum

class ParameterID(Enum):
    DELAY = 0
    DC = 1
    AC = 2
    FREQUENCY = 3
    PRESSURE = 4
    INSTEK_V_1 = 5
    INSTEK_V_2 = 6
    RUDI_1 = 7
    RUDI_2 = 8
    RUDI_3 = 9
    RUDI_4 = 10
    KEITHLEY_V = 11
    KEITHLEY_I = 12

class Parameter:
    def __init__(self, id: ParameterID, name: str, unit: str, editable: bool, minimum: float, maximum: float):
        self.id = id
        self.name = name
        self.unit = unit
        self.editable = editable
        self.minimum = minimum
        self.maximum = maximum