from enum import Enum
from parameter import ParameterID


class StartCommand:
    def __init__(self, title: str, comment: str):
        self.title: str = title
        self.comment: str = comment


class PauseCommand:
    def __init__(self):
        pass


class StopCommand:
    def __init__(self):
        pass


class SweepCommand:
    def __init__(self):
        self.enabledOne: bool = False
        self.enabledTwo: bool = False

        self.paramOne: ParameterID() = None
        self.paramTwo: ParameterID() = None
        self.minOne: float = None
        self.minTwo: float = None
        self.maxOne: float = None
        self.maxTwo: float = None
        self.stepsOne: int = None
        self.stepsTwo: int = None

    def addSweepOne(
        self, param: ParameterID, minimum: float, maximum: float, steps: int
    ):
        self.enabledOne = True
        self.paramOne = param
        self.minOne = minimum
        self.maxOne = maximum
        self.stepsOne = steps

        return self

    def addSweepOne(
        self, param: ParameterID, minimum: float, maximum: float, steps: int
    ):
        self.enabledOne = True
        self.paramTwo = param
        self.minTwo = minimum
        self.maxTwo = maximum
        self.stepsTwo = steps

        return self


class ParamCommand:
    def __init__(self, param: ParameterID, value: float):
        self.param: ParameterID = param
        self.value: float = value
