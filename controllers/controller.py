from parameter import ParameterID, Parameter
import math
import time


class Controller:
    def __init__(self):
        pass

    def getHandled(self) -> dict[ParameterID, Parameter]:
        pass

    def connect(self) -> bool:
        pass

    def adjust(self, param: ParameterID, value: float) -> None:
        pass

    def read(self, param: ParameterID) -> float:
        pass

    def enable(self, state: bool) -> None:
        pass


class DummyController(Controller):
    def __init__(self):
        self.ac = 0
        self.dc = 0
        self.pressure = 0
        self.frequency = 0
        self.current = 0

    def getHandled(self):
        return {
            ParameterID.AC: Parameter(ParameterID.AC, "AC Gen", "V", True, 0, 20),
            ParameterID.DC: Parameter(ParameterID.DC, "DC Gen", "V", True, 0, 20),
            ParameterID.FREQUENCY: Parameter(ParameterID.FREQUENCY, "Frequency Gen", "Hz", True, 0, 20e6),
        }

    def adjust(self, param: ParameterID, value: float) -> None:
        print(f"Adjusting {param} to {value}")
        if param == ParameterID.AC:
            self.ac = value
        if param == ParameterID.DC:
            self.dc = value
        if param == ParameterID.FREQUENCY:
            self.frequency = value
        if param == ParameterID.PRESSURE:
            self.pressure = value

    def connect(self) -> bool:
        return True

    def read(self, param: ParameterID) -> float:
        if param == ParameterID.AC:
            return self.dc**2
        if param == ParameterID.DC:
            return self.dc
        if param == ParameterID.FREQUENCY:
            return self.frequency
        if param == ParameterID.CURRENT:
            return math.sin(time.time())