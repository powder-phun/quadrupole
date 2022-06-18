from PySide6.QtWidgets import QMainWindow, QComboBox
from PySide6.QtCore import Slot, Signal, QThread
from PySide6.QtTest import QSignalSpy
from ui.main_window import Ui_MainWindow

from parameter import ParameterID, Parameter
from utils import FLOAT_VALIDATOR
from executor import Executor


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.params: dict[ParameterID, Parameter] = {}
        self.setupParams()

        self.started: bool = False
        self.paused = False

        self.executor = Executor()
        self.executorThread = QThread()
        self.executor.moveToThread(self.executorThread)

        self.initializeUI()

        self.connectAll()

        self.executorThread.start()

    # Initialize everything such as ParamDock, SweepWidget
    def initializeUI(self):
        self.ui.paramDock.fill(self.params)

        # Setting-up sweepWidget
        self.ui.sweepWidget.params = self.params
        self.ui.sweepWidget.fillComboboxes()

    def connectAll(self):
        self.ui.startButton.clicked.connect(self.startClicked)
        self.ui.stopButton.clicked.connect(self.stopClicked)

        self.ui.sweepWidget.selectedOneChanged.connect(self.sweepOneChanged)
        self.ui.sweepWidget.selectedTwoChanged.connect(self.sweepTwoChanged)

        self.executorThread.started.connect(self.executor.connect)
        self.ui.paramDock.valueSet.connect(self.executor.adjust)

    @Slot(ParameterID, ParameterID)
    def sweepOneChanged(self, identifier, old):
        if identifier is not None:
            self.ui.paramDock.setEnabledParam(identifier, False)
        if old is not None:
            self.ui.paramDock.setEnabledParam(old, True)

    @Slot(ParameterID, ParameterID)
    def sweepTwoChanged(self, identifier, old):
        if identifier is not None:
            self.ui.paramDock.setEnabledParam(identifier, False)
        if old is not None:
            self.ui.paramDock.setEnabledParam(old, True)

    def startClicked(self):
        if not self.started and not self.paused:
            self.started = True
            self.paused = False

            self.ui.startButton.setText("Pause")
            self.ui.stopButton.setEnabled(False)

            # TODO: Send sweep data

            # TODO: Start measurement

        elif self.started and not self.paused:
            self.started = False
            self.paused = True

            self.ui.startButton.setText("Re-start")
            self.ui.stopButton.setEnabled(True)

            # TODO: Pause measurement

        elif self.paused:
            self.paused = False
            self.started = True

            self.ui.startButton.setText("Pause")
            self.ui.stopButton.setEnabled(False)

            # TODO: Restart measurement

    def stopClicked(self):
        self.started = False
        self.paused = False

        self.ui.startButton.setText("Start")
        self.ui.stopButton.setEnabled(False)

        # TODO: Stop measurement

    def setupParams(self):
        self.params[ParameterID.DC] = Parameter(ParameterID.DC, "DC", "V", True, 0, 20)
        self.params[ParameterID.AC] = Parameter(ParameterID.AC, "AC", "V", True, 0, 20)
        self.params[ParameterID.DELAY] = Parameter(
            ParameterID.DELAY, "Delay", "s", True, 0, 100
        )
        self.params[ParameterID.PRESSURE] = Parameter(
            ParameterID.PRESSURE, "Pressure", "mbar", True, 0, 1e-2
        )
        self.params[ParameterID.CURRENT] = Parameter(
            ParameterID.CURRENT, "Ion Current", "A", False, None, None
        )
