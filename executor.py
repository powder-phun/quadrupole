from PySide6.QtCore import QObject, Slot, QTimer, Signal
import time
import datetime
import csv

from parameter import Parameter
from controllers.controller import Controller
from controllers.dummyController import DummyController
from config import Config, ControllerConfig

from utils import DataPacket


class Executor(QObject):
    exited = Signal()
    measured = Signal(DataPacket)
    stoped = Signal()
    controllersConnected = Signal(object)

    def __init__(self, config, parent: QObject = None):
        super(Executor, self).__init__(parent)

        self.config: Config = config
        
        self.controllerTemplates: dict[str, Controller] = {}
        self.controllers: dict[str, Controller] = {}
        self.params:dict[str, Parameter] = {}
        self.timer = None
        self.delay = 0.1
        self.counter = 0
        self.startTime = time.time()

        self.file = None
        self.title = None
        self.comment = None

        self.sweepOneEnabled: bool = False
        self.sweepOneParam: str = None
        self.sweepOneMin: float = 0
        self.sweepOneMax: float = 0
        self.sweepOneSteps: int = 2

        self.sweepTwoEnabled: bool = False
        self.sweepTwoParam: str = None
        self.sweepTwoMin: float = 0
        self.sweepTwoMax: float = 0
        self.sweepTwoSteps: int = 2

        self.fileSweepEnabled: bool = False
        self.fileSweepName: str = ""

        self.fileSweepData: dict(str, list(float)) = {}
        self.fileSweepSteps: int = 0

        self.sweepTwoValue = 0

    def initControllers(self) -> None:
        self.controllerTemplates[DummyController.getName()] = DummyController
        # pressure = PressureController()
        # self.addController(pressure)
        # keithley = KeithleyVControllerReversed()
        # self.addController(keithley)
        # tek = TekController()
        # self.addController(tek)
        # instek = InstekController()
        # self.addController(instek)
        # rudi = RudiController()
        # self.addController(rudi)
        # keithley_voltage = KeithleyIController()
        # self.addController(keithley_voltage)
        # sdm = SDMController()
        # self.addController(sdm)
        for controller in self.config.controllers:
            self.addController(self.controllerTemplates[controller.type](controller), controller)
            

    def addController(self, controller: Controller, config: ControllerConfig) -> None:
        params = controller.getHandled()
        if controller.connect():
            for identifier, key in params.items():
                self.controllers[identifier] = controller
                self.params[identifier] = key


        self.params["Delay"] = Parameter("Delay", "s", True, 0, 10000)

    @Slot()
    def connectControllers(self):
        self.initControllers()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.setInterval(10)
        self.controllersConnected.emit(self.params)

    def loop(self):
        self.timer.stop()

        self.setParameters()

        if self.file is None:
            self.openFile()

        time.sleep(self.delay)
        packet = DataPacket(time.time() - self.startTime, self.counter)
        for param in self.controllers.keys():
            packet.addData(param, self.read(param))

        line = ""
        for param, value in packet.data.items():
            line += str(value) + "\t"
        line += "\n"
        self.file.write(line)

        self.measured.emit(packet)
        self.counter += 1

        if self.sweepTwoEnabled:
            if self.counter % self.sweepOneSteps == 0:
                self.file.close()
                self.file = None

        # Handle stopping
        if self.sweepTwoEnabled and self.sweepOneEnabled:
            if self.counter == self.sweepOneSteps * self.sweepTwoSteps:
                self.stop()
            else:
                self.timer.start()
        elif self.sweepOneEnabled:
            if self.counter == self.sweepOneSteps:
                self.stop()
            else:
                self.timer.start()
        elif self.fileSweepEnabled:
            if self.counter == self.fileSweepSteps:
                self.stop()
            else:
                self.timer.start()
        else:
            self.timer.start()

    def read(self, param: str) -> float:
        return self.controllers[param].read(param)


    def setParameters(self) -> None:
        sweepOneIndex = self.counter % self.sweepOneSteps
        sweepTwoIndex = self.counter // self.sweepOneSteps

        if self.sweepOneEnabled:
            value = (sweepOneIndex/(self.sweepOneSteps-1)) * (self.sweepOneMax-self.sweepOneMin) + self.sweepOneMin
            self.adjust(self.sweepOneParam, value)

        if self.sweepTwoEnabled:
            value = (sweepTwoIndex/(self.sweepTwoSteps-1)) * (self.sweepTwoMax-self.sweepTwoMin) + self.sweepTwoMin
            self.sweepTwoValue = value
            self.adjust(self.sweepTwoParam)

        if self.fileSweepEnabled:
            for param, values in self.fileSweepData.items():
                self.adjust(param, values[self.counter])


    @Slot(str, float)
    def adjust(self, param: str, value: float) -> None:
        if param == "Delay":
            self.delay = value
        else:
            self.controllers[param].adjust(param, value)

    @Slot(str, str)
    def start(self, title, comment) -> None:
        self.timer.start()
        self.startTime = time.time()

        self.title = title
        self.comment = comment


    @Slot()
    def pause(self) -> None:
        self.timer.stop()

    @Slot()
    def stop(self) -> None:
        self.timer.stop()
        if self.file is not None:
            self.file.close()
            self.file = None

        self.counter = 0
        self.stoped.emit()

    @Slot()
    def restart(self) -> None:
        self.timer.start()

    @Slot()
    def exit(self):
        self.timer.stop()
        self.exited.emit()

    @Slot(bool, str, float, float, int)
    def sweepOneSet(self, enabled: bool, param: str = None, minimum: float = 0, maximum: float = 0, steps: int = 2):
        self.sweepOneEnabled = enabled
        self.sweepOneParam = param
        self.sweepOneMin = minimum
        self.sweepOneMax = maximum
        self.sweepOneSteps = steps

    @Slot(bool, str, float, float, int)
    def sweepTwoSet(self, enabled: bool, param: str = None, minimum: float = 0, maximum: float = 0, steps: int = 2):
        self.sweepTwoEnabled = enabled
        self.sweepTwoParam = param
        self.sweepTwoMin = minimum
        self.sweepTwoMax = maximum
        self.sweepTwoSteps = steps

    @Slot(bool, str)
    def fileSweepSet(self, enabled: bool, filename: str):
        self.fileSweepEnabled = enabled
        self.fileSweepName = filename
        print(self.fileSweepName)

        with open(filename, encoding='utf-8-sig') as f:
            reader = csv.reader(f, skipinitialspace=True, dialect="excel")
            header = next(reader)

            # Read in header as list of parameter ID's
            list_of_params = []
            for name in header:
                param = next((param for param in self.params.values() if param.name == name), None)
                if param is not None:
                    list_of_params.append(param.name)
                else:
                    list_of_params.append(None)
                    print(f'[Executor][Error] No param named "{name}" found')

            # Create empty list for each parameter
            for param in list_of_params:
                self.fileSweepData[param] = []

            # Fill in values for parameters and count rows
            self.fileSweepSteps = 0
            for row in reader:
                self.fileSweepSteps += 1
                for index, value in enumerate(row):
                    self.fileSweepData[list_of_params[index]].append(float(value))

    def openFile(self):
        t = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        p = ""
        if self.sweepTwoEnabled:
            val = (str(self.sweepTwoValue)).replace(".","dot")
            p = f"{self.params[self.sweepOneParam].name}-{val}"

        self.file = open("data/"+t+self.title+p, 'w+')

        self.file.write(f"# {self.comment}\n")

        header = ""
        for param in self.params.values():
            header += param.name + "\t"

        self.file.write(header)
        self.file.write("\n")

    @Slot(bool)
    def enable(self, bool):
        controllerSet = set(self.controllers.values())
        for controller in controllerSet:
            controller.enable(bool)