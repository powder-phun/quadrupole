from PySide6.QtWidgets import QMainWindow, QComboBox
from PySide6.QtCore import Slot, Signal, QThread
from PySide6.QtTest import QSignalSpy
from ui.main_window import Ui_MainWindow

from parameter import ParameterID, Parameter
from utils import FLOAT_VALIDATOR, State, DataPacket
from executor import Executor


class Main(QMainWindow):
    started = Signal(str, str)
    stoped = Signal()
    paused = Signal()
    restarted = Signal()

    sweepOneSetup = Signal((bool,), (bool, ParameterID, float, float, int))
    sweepTwoSetup = Signal((bool,), (bool, ParameterID, float, float, int))

    exited = Signal()

    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.params: dict[ParameterID, Parameter] = {}
        self.setupParams()

        self.state = State.STOPPED

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

        # Setting up timeChart
        self.ui.timeChart.setup(self.params)
        # Setting up twoDChart
        self.ui.twoDChart.setup(self.params)

    def connectAll(self):
        self.ui.startButton.clicked.connect(self.startClicked)
        self.ui.stopButton.clicked.connect(self.stopClicked)

        self.ui.sweepWidget.selectedOneChanged.connect(self.sweepOneChanged)
        self.ui.sweepWidget.selectedTwoChanged.connect(self.sweepTwoChanged)

        self.executorThread.started.connect(self.executor.connectControllers)

        self.ui.paramDock.valueSet.connect(self.executor.adjust)

        self.started.connect(self.executor.start)
        self.paused.connect(self.executor.pause)
        self.restarted.connect(self.executor.restart)
        self.stoped.connect(self.executor.stop)
        self.exited.connect(self.executor.exit)

        self.executor.exited.connect(self.executorThread.terminate)
        self.executor.exited.connect(self.executor.deleteLater)
        self.executor.exited.connect(self.executorThread.deleteLater)
        self.executor.exited.connect(self.close)

        self.executor.measured.connect(self.dataMeasured)

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
        if self.state == State.STOPPED:
            self.state = State.RUNNING

            self.ui.startButton.setText("Pause")
            self.ui.stopButton.setEnabled(False)
            self.ui.sweepWidget.setEnabledEverything(False)

            # TODO: Send sweep data

            self.started.emit(
                self.ui.titleEdit.text(), self.ui.commentEdit.toPlainText()
            )

        elif self.state == State.RUNNING:
            self.state = State.PAUSED

            self.ui.startButton.setText("Re-start")
            self.ui.stopButton.setEnabled(True)

            self.paused.emit()

        elif self.state == State.PAUSED:
            self.state = State.RUNNING

            self.ui.startButton.setText("Pause")
            self.ui.stopButton.setEnabled(False)

            self.restarted.emit()

    def stopClicked(self):
        self.state = State.STOPPED

        self.ui.startButton.setText("Start")
        self.ui.stopButton.setEnabled(False)
        self.ui.sweepWidget.setEnabledEverything(True)

        self.ui.timeChart.clear()

        self.stoped.emit()

    def setupParams(self):
        self.params[ParameterID.DC] = Parameter(ParameterID.DC, "DC", "V", True, 0, 20)
        self.params[ParameterID.AC] = Parameter(ParameterID.AC, "AC", "V", True, 0, 20)
        self.params[ParameterID.FREQUENCY] = Parameter(
            ParameterID.FREQUENCY, "Frequency", "Hz", True, 0, 20e6
        )
        self.params[ParameterID.DELAY] = Parameter(
            ParameterID.DELAY, "Delay", "s", True, 0, 100
        )
        self.params[ParameterID.PRESSURE] = Parameter(
            ParameterID.PRESSURE, "Pressure", "mbar", True, 0, 1e-2
        )
        self.params[ParameterID.CURRENT] = Parameter(
            ParameterID.CURRENT, "Ion Current", "A", False, -1, 1
        )

    def closeEvent(self, event):
        self.exited.emit()

    @Slot(DataPacket)
    def dataMeasured(self, packet):
        for param, value in packet.data.items():
            self.ui.paramDock.setData(param, value)

        self.ui.timeChart.addData(packet)
        self.ui.twoDChart.addData(packet)
