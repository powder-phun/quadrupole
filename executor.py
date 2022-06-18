from PySide6.QtCore import QObject, Slot, QTimer
from multiprocessing import Queue


from parameter import ParameterID
from controller import Controller, DummyController

from threading import get_native_id


class Executor(QObject):
    def __init__(self, parent: QObject = None):
        super(Executor, self).__init__(parent)
        self.controllers: dict[ParameterID, Controller] = {}
        self.initControllers()
        self.running: bool = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.setInterval(10)

    def initControllers(self) -> None:
        dummy = DummyController()
        self.addController(dummy)

    def addController(self, controller: Controller) -> None:
        params = controller.getHandled()
        for param in params:
            self.controllers[param] = controller

    @Slot()
    def connect(self):
        for controller in self.controllers.values():
            controller.connect()

    def loop(self):
        self.timer.stop()
        packet = DataPacket()
        for param in self.controllers.keys():
            packet.add_param(param, self.read(param))
        self.timer.start()

    def read(self, param: ParameterID) -> float:
        return self.controllers[param].read(param)

    @Slot(ParameterID, float)
    def adjust(self, param: ParameterID, value: float) -> None:
        if param == ParameterID.DELAY:
            self.delay = value
        else:
            self.controllers[param].adjust(param, value)

    @Slot(str, str)
    def start(self, title, comment) -> None:
        self.timer.start()

        # TODO: Save title and comment and prepare everything for measurement

    @Slot()
    def pause(self) -> None:
        self.timer.stop()

    @Slot()
    def stop(self) -> None:
        self.timer.stop()

        # TODO: Reset everything

    @Slot()
    def restart(self) -> None:
        self.timer.start()
