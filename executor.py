from PySide6.QtCore import QObject, Slot, QTimer, Signal
import time

from parameter import ParameterID
from controller import Controller, DummyController
from utils import DataPacket


class Executor(QObject):
    exited = Signal()
    measured = Signal(DataPacket)

    def __init__(self, parent: QObject = None):
        super(Executor, self).__init__(parent)
        self.controllers: dict[ParameterID, Controller] = {}
        self.initControllers()
        self.timer = None
        self.delay = 0.1
        self.counter = 0
        self.startTime = time.time()

    def initControllers(self) -> None:
        dummy = DummyController()
        self.addController(dummy)

    def addController(self, controller: Controller) -> None:
        params = controller.getHandled()
        for param in params:
            self.controllers[param] = controller

    @Slot()
    def connectControllers(self):
        for controller in self.controllers.values():
            controller.connect()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.setInterval(10)

    def loop(self):
        self.timer.stop()

        time.sleep(self.delay)
        packet = DataPacket(time.time() - self.startTime, self.counter)
        for param in self.controllers.keys():
            packet.addData(param, self.read(param))

        self.measured.emit(packet)
        self.counter += 1

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
        self.startTime = time.time()

        # TODO: Save title and comment and prepare everything for measurement

    @Slot()
    def pause(self) -> None:
        self.timer.stop()

    @Slot()
    def stop(self) -> None:
        self.timer.stop()

        self.counter = 0
        # TODO: Reset everything

    @Slot()
    def restart(self) -> None:
        self.timer.start()

    @Slot()
    def exit(self):
        self.timer.stop()
        self.exited.emit()
