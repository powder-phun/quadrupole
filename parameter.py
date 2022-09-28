from enum import Enum

class Parameter:
    def __init__(self, name: str, unit: str, editable: bool, minimum: float, maximum: float):
        self.name = name
        self.unit = unit
        self.editable = editable
        self.minimum = minimum
        self.maximum = maximum