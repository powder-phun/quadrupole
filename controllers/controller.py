from parameter import Parameter
import math
import time


class Controller:
    def __init__(self, config):
        pass

    @staticmethod
    def getName() -> str:
        pass
    
    def getHandled(self) -> dict:
        pass

    def connect(self) -> bool:
        pass

    def adjust(self, param: str, value: float) -> None:
        pass

    def read(self, param: str) -> float:
        pass

    def enable(self, state: bool) -> None:
        pass


