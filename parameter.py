from enum import Enum

class ParameterID(Enum):
    DELAY = 0
    DC = 1
    AC = 2
    FREQUENCY = 3
    PRESSURE = 4
    CURRENT = 5
    HV_DETECTOR = 6
    INSTEK_V_1 = 7
    INSTEK_V_2 = 8

class Parameter:
    def __init__(self, id: ParameterID, name: str, unit: str, editable: bool, minimum: float, maximum: float):
        self.id = id
        self.name = name
        self.unit = unit
        self.editable = editable
        self.minimum = minimum
        self.maximum = maximum