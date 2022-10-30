class Controller:
    def __init__(self, config):
        pass

    @staticmethod
    def getName() -> str:
        pass
    
    @staticmethod
    def getIsEditableDict() -> dict[str, bool]:
        pass
    
    @staticmethod
    def getUnitDict() -> dict[str, str]:
        pass

    def connect(self) -> bool:
        pass

    def adjust(self, param: str, value: float) -> None:
        pass

    def read(self, param: str) -> float:
        pass

    def enable(self, state: bool) -> None:
        pass


