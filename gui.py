from PySide6.QtWidgets import QMainWindow, QComboBox
from PySide6.QtCore import Slot, Signal, QThread
from PySide6.QtTest import QSignalSpy
from ui.main_window import Ui_MainWindow

import os
import csv
import logging

from config import ParamConfig
from utils import FLOAT_VALIDATOR, State, DataPacket
from executor import Executor


class Main(QMainWindow):
    started = Signal(str, str)
    stoped = Signal()
    paused = Signal()
    restarted = Signal()
    enableDevicesChanged = Signal(bool)

    sweepOneSetup = Signal(bool, str, float, float, int)
    sweepTwoSetup = Signal(bool, str, float, float, int)
    fileSweepSetup = Signal(bool, str)

    exited = Signal()

    def __init__(self, config):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.config = config

        self.params: dict[str, ParamConfig] = {}
        
        self.state = State.STOPPED

        self.showMaximized()

        self.executor = Executor(config)
        self.executorThread = QThread()
        self.executor.moveToThread(self.executorThread)

        self.connectAll()

        self.devicesEnabled: bool = False

        self.executorThread.start()

        self.fileSweepParams: list(str) = []
        self.fileSweepSteps: int = 0

    # Initialize everything such as ParamDock, SweepWidget

    def initializeUI(self, params):
        self.params = params

        self.ui.paramDock.fill(self.params)

        # Setting-up sweepWidget
        self.ui.sweepWidget.params = self.params
        self.ui.sweepWidget.fillComboboxes()
        self.ui.sweepWidget.setDefaults(self.config.defaults)

        # Setting up timeChart
        self.ui.timeChart.setup(self.params)
        # Setting up twoDChart
        self.ui.twoDChart.setup(self.params)
        # Setting up threeDChart
        self.ui.threeDChart.setup(self.params)

    def connectAll(self):
        self.ui.startButton.clicked.connect(self.startClicked)
        self.ui.stopButton.clicked.connect(self.stopClicked)
        self.ui.enableButton.clicked.connect(self.enableClicked)

        self.ui.sweepWidget.selectedOneChanged.connect(self.sweepOneChanged)
        self.ui.sweepWidget.selectedTwoChanged.connect(self.sweepTwoChanged)

        self.executorThread.started.connect(self.executor.connectControllers)

        self.ui.paramDock.valueSet.connect(self.executor.adjust)

        self.started.connect(self.executor.start)
        self.paused.connect(self.executor.pause)
        self.restarted.connect(self.executor.restart)
        self.stoped.connect(self.executor.stop)
        self.exited.connect(self.executor.exit)
        self.sweepOneSetup.connect(self.executor.sweepOneSet)
        self.sweepTwoSetup.connect(self.executor.sweepTwoSet)
        self.fileSweepSetup.connect(self.executor.fileSweepSet)
        self.enableDevicesChanged.connect(self.executor.enable)

        self.executor.exited.connect(self.executorThread.terminate)
        self.executor.exited.connect(self.executor.deleteLater)
        self.executor.exited.connect(self.executorThread.deleteLater)
        self.executor.exited.connect(self.close)

        self.executor.controllersConnected.connect(self.initializeUI)
        self.executor.measured.connect(self.dataMeasured)
        self.executor.stoped.connect(self.stopMeasurement)

        self.ui.sweepWidget.ui.fileSweepLineEdit.textChanged.connect(self.sweepFileSelected)
        self.ui.sweepWidget.ui.fileSweepCheckbox.stateChanged.connect(self.fileSweepEnabled)

    @Slot(object, object)
    def sweepOneChanged(self, identifier, old):
        if identifier is not None:
            self.ui.paramDock.setEnabledParam(identifier, False)
        if old is not None:
            self.ui.paramDock.setEnabledParam(old, True)

    @Slot(object, object)
    def sweepTwoChanged(self, identifier, old):
        if identifier is not None:
            self.ui.paramDock.setEnabledParam(identifier, False)
        if old is not None:
            self.ui.paramDock.setEnabledParam(old, True)

    def fileSweepChanged(self, new_list, old_list):
        for param in old_list:
            self.ui.paramDock.setEnabledParam(param, True)
        for param in new_list:
            self.ui.paramDock.setEnabledParam(param, False)


    def startClicked(self):
        if self.state == State.STOPPED:
            self.state = State.RUNNING

            self.ui.twoDChart.clear()
            self.ui.timeChart.clear()

            self.enableDevices(True)

            self.ui.startButton.setText("Pause")
            self.ui.stopButton.setEnabled(False)
            self.ui.progressBar.setEnabled(True)
            self.ui.sweepWidget.setEnabledEverything(False)

            if self.ui.sweepWidget.ui.sweepOneCheckbox.isChecked():
                self.sweepOneSetup.emit(
                    self.ui.sweepWidget.ui.sweepOneCheckbox.isChecked(),
                    self.ui.sweepWidget.selectedOne,
                    float(self.ui.sweepWidget.ui.sweepOneMinEdit.text()),
                    float(self.ui.sweepWidget.ui.sweepOneMaxEdit.text()),
                    self.ui.sweepWidget.ui.sweepOneStepsSpinbox.value(),
                )
            else:
                self.sweepOneSetup.emit(False, None, 0, 0, 2)

            if self.ui.sweepWidget.ui.sweepTwoCheckbox.isChecked():
                self.sweepTwoSetup.emit(
                    self.ui.sweepWidget.ui.sweepTwoCheckbox.isChecked(),
                    self.ui.sweepWidget.selectedTwo,
                    float(self.ui.sweepWidget.ui.sweepTwoMinEdit.text()),
                    float(self.ui.sweepWidget.ui.sweepTwoMaxEdit.text()),
                    self.ui.sweepWidget.ui.sweepTwoStepsSpinbox.value(),
                )
            else:
                self.sweepTwoSetup.emit(False, None, 0, 0, 2)

            if self.ui.sweepWidget.ui.fileSweepCheckbox.isChecked():
                self.fileSweepSetup.emit(True, self.ui.sweepWidget.ui.fileSweepLineEdit.text())
            else:
                self.fileSweepSetup.emit(False, "")

            if self.ui.sweepWidget.ui.sweepOneCheckbox.isChecked() and self.ui.sweepWidget.ui.sweepTwoCheckbox.isChecked():
                self.ui.threeDChart.setRanges(
                    self.ui.sweepWidget.selectedOne,
                    self.ui.sweepWidget.selectedTwo,
                    float(self.ui.sweepWidget.ui.sweepOneMinEdit.text()),
                    float(self.ui.sweepWidget.ui.sweepOneMaxEdit.text()),
                    self.ui.sweepWidget.ui.sweepOneStepsSpinbox.value(),
                    float(self.ui.sweepWidget.ui.sweepTwoMinEdit.text()),
                    float(self.ui.sweepWidget.ui.sweepTwoMaxEdit.text()),
                    self.ui.sweepWidget.ui.sweepTwoStepsSpinbox.value()
                )

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
        self.stopMeasurement()     

        self.stoped.emit()

    def enableClicked(self):
        self.enableDevices(not self.devicesEnabled)

    def enableDevices(self, val):
        if val:
            self.devicesEnabled = True
            self.ui.enableButton.setText("Disable")
            self.enableDevicesChanged.emit(True)

        else:
            self.devicesEnabled = False
            self.ui.enableButton.setText("Enable")
            self.enableDevicesChanged.emit(False)


    @Slot()
    def stopMeasurement(self):
        self.state = State.STOPPED

        self.enableDevices(False)

        self.ui.startButton.setText("Start")
        self.ui.stopButton.setEnabled(False)
        self.ui.sweepWidget.setEnabledEverything(True)

        self.ui.progressBar.setEnabled(False)


    def closeEvent(self, event):
        self.exited.emit()

    @Slot(DataPacket)
    def dataMeasured(self, packet: DataPacket):
        self.setProgress(packet.step, packet.timestamp)

        for param, value in packet.data.items():
            self.ui.paramDock.setData(param, value)
        self.ui.timeChart.addData(packet)
        self.ui.twoDChart.addData(packet)
        if self.ui.sweepWidget.ui.sweepTwoCheckbox.isChecked():
            self.ui.threeDChart.addData(packet)

    def setProgress(self, steps, timestamp):
        steps += 1
        stepsMax = 1
        stepsMax *= self.ui.sweepWidget.ui.sweepOneStepsSpinbox.value() if self.ui.sweepWidget.ui.sweepOneCheckbox.isChecked() else 1
        stepsMax *= self.ui.sweepWidget.ui.sweepTwoStepsSpinbox.value() if self.ui.sweepWidget.ui.sweepTwoCheckbox.isChecked() else 1
        stepsMax *= self.fileSweepSteps if self.ui.sweepWidget.ui.fileSweepCheckbox.isChecked() else 1

        self.ui.stepCountLabel.setText(f"{steps}/{stepsMax}")
        seconds = int(timestamp/steps * (stepsMax-steps))
        seconds_left = seconds % 60
        minutes = seconds // 60
        minutes_left = minutes % 60
        hours = minutes // 60

        self.ui.timeLeftLabel.setText(f"{hours}:{minutes_left}:{seconds_left}")

        self.ui.progressBar.setValue(steps/stepsMax * 100)

    def sweepFileSelected(self, filename):
        old = self.fileSweepParams
        if os.path.exists(filename):
            with open(filename, encoding='utf-8-sig') as f:
                reader = csv.reader(f, skipinitialspace=True, dialect="excel")
                header = next(reader)

                # Read in header as list of parameter ID's
                self.fileSweepParams = []
                for name in header:
                    param = next((param for param in self.params.values() if param.name == name), None)
                    if param is not None:
                        self.fileSweepParams.append(param.name)
                    else:
                        logging.error(f'No param named "{name}" found')
                
                self.fileSweepSteps = 0
                for row in reader:
                    self.fileSweepSteps += 1

        else:
            self.fileSweepParams = []
            self.fileSweepSteps = 0
        self.fileSweepChanged(self.fileSweepParams, old)

    def fileSweepEnabled(self, value):
        if value:
            self.fileSweepChanged(self.fileSweepParams, [])
        else:
            self.fileSweepChanged([], self.fileSweepParams)