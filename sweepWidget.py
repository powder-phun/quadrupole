from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Signal

from ui.sweep_widget import Ui_sweepWidget
from utils import FLOAT_VALIDATOR
from parameter import Parameter


class SweepWidget(QWidget):
    selectedOneChanged = Signal(object, object)
    selectedTwoChanged = Signal(object, object)

    def __init__(self, parent=None):
        super(SweepWidget, self).__init__(parent)
        self.ui = Ui_sweepWidget()
        self.ui.setupUi(self)

        self.selectedOne: str = None
        self.selectedTwo: str = None

        self.selectingCallbackEnabled = True

        self.params: dict[str, Parameter] = None

        self.ui.sweepOneMinEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepOneMaxEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepTwoMinEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepTwoMaxEdit.setValidator(FLOAT_VALIDATOR)

        self.connectAll()

    def connectAll(self):
        self.ui.sweepOneCheckbox.stateChanged.connect(self.checkboxOneClicked)
        self.ui.sweepTwoCheckbox.stateChanged.connect(self.checkboxTwoClicked)
        self.ui.fileSweepCheckbox.stateChanged.connect(self.checkboxFileClicked)

        self.ui.sweepOneCombobox.currentTextChanged.connect(self.comboboxOneChanged)
        self.ui.sweepTwoCombobox.currentTextChanged.connect(self.comboboxTwoChanged)

        self.ui.fileSweepOpenPushbutton.clicked.connect(self.openFileClicked)

    def setDefaults(self, defaults):
        if "sweepOne" in defaults:
            if "param" in defaults["sweepOne"]:
                self.ui.sweepOneCombobox.setCurrentIndex(
                    self.ui.sweepOneCombobox.findText(defaults["sweepOne"]["param"])
                )
            if "enabled" in defaults["sweepOne"] and defaults["sweepOne"]["enabled"]:
                self.ui.sweepOneCheckbox.setChecked(True)
            if "min" in defaults["sweepOne"]:
                self.ui.sweepOneMinEdit.setText(str(defaults["sweepOne"]["min"]))
            if "max" in defaults["sweepOne"]:
                self.ui.sweepOneMaxEdit.setText(str(defaults["sweepOne"]["max"]))
            if "steps" in defaults["sweepOne"]:
                self.ui.sweepOneStepsSpinbox.setValue(int(defaults["sweepOne"]["steps"]))

        if "sweepTwo" in defaults:
            if "param" in defaults["sweepTwo"]:
                self.ui.sweepTwoCombobox.setCurrentIndex(
                    self.ui.sweepTwoCombobox.findText(defaults["sweepTwo"]["param"])
                )
            if "enabled" in defaults["sweepTwo"] and defaults["sweepTwo"]["enabled"]:
                self.ui.sweepTwoCheckbox.setChecked(True)
            if "min" in defaults["sweepTwo"]:
                self.ui.sweepTwoMinEdit.setText(str(defaults["sweepTwo"]["min"]))
            if "max" in defaults["sweepTwo"]:
                self.ui.sweepTwoMaxEdit.setText(str(defaults["sweepTwo"]["max"]))
            if "steps" in defaults["sweepTwo"]:
                self.ui.sweepTwoStepsSpinbox.setValue(int(defaults["sweepTwo"]["steps"]))

        if "fileSweep" in defaults:
            if "enabled" in defaults["fileSweep"] and defaults["fileSweep"]["enabled"]:
                self.ui.fileSweepCheckbox.setChecked(True)
            if "file" in defaults["fileSweep"]:
                self.ui.fileSweepLineEdit.setText(defaults["fileSweep"]["file"])



    def fillComboboxes(self):
        # Disable callback on change
        self.selectingCallbackEnabled = False

        # Clear comboboxes from previous
        self.ui.sweepOneCombobox.clear()
        self.ui.sweepTwoCombobox.clear()

        # Fill comboboxes
        for param in self.params.values():
            if param.editable:
                if param.name != self.selectedOne and param.name:
                    self.ui.sweepTwoCombobox.addItem(param.name)
                if param.name != self.selectedTwo and param.name:
                    self.ui.sweepOneCombobox.addItem(param.name)

        # Select the correct one
        if self.selectedOne is not None:
            self.ui.sweepOneCombobox.setCurrentIndex(
                self.ui.sweepOneCombobox.findText(self.params[self.selectedOne].name)
            )
        if self.selectedTwo is not None:
            self.ui.sweepTwoCombobox.setCurrentIndex(
                self.ui.sweepTwoCombobox.findText(self.params[self.selectedTwo].name)
            )
        # Re-enable callback
        self.selectingCallbackEnabled = True

    def setEnabledOne(self, value):
        self.ui.sweepOneCombobox.setEnabled(value)
        self.ui.sweepOneMinEdit.setEnabled(value)
        self.ui.sweepOneMaxEdit.setEnabled(value)
        self.ui.sweepOneStepsSpinbox.setEnabled(value)

        # Set selected one based on current text
        if value:
            self.setSelectedOne(self.ui.sweepOneCombobox.currentText())
        else:
            self.setSelectedOne(None)

        # Re-setup comboboxes
        self.fillComboboxes()

    def setEnabledTwo(self, value):
        self.ui.sweepTwoCombobox.setEnabled(value)
        self.ui.sweepTwoMinEdit.setEnabled(value)
        self.ui.sweepTwoMaxEdit.setEnabled(value)
        self.ui.sweepTwoStepsSpinbox.setEnabled(value)

        # Set selected one based on current text
        if value:
            self.setSelectedTwo(self.ui.sweepTwoCombobox.currentText())
        else:
            self.setSelectedTwo(None)

        # Re-setup comboboxes
        self.fillComboboxes()

    def setEnabledFile(self, value):
        self.ui.fileSweepAddSpinBox.setEnabled(value)
        self.ui.fileSweepLineEdit.setEnabled(value)
        self.ui.fileSweepMultiplySpinbox.setEnabled(value)
        self.ui.fileSweepOpenPushbutton.setEnabled(value)

    def setEnabledEverything(self, value):
        if value:
            # Enable sweep one only if checkbox selected
            if self.ui.sweepOneCheckbox.isChecked():
                self.ui.sweepTwoCheckbox.setEnabled(True)

                self.ui.sweepOneCombobox.setEnabled(True)
                self.ui.sweepOneMinEdit.setEnabled(True)
                self.ui.sweepOneMaxEdit.setEnabled(True)
                self.ui.sweepOneStepsSpinbox.setEnabled(True)

            # Enable sweep two only if checkbox selected
            if self.ui.sweepTwoCheckbox.isChecked():
                self.ui.sweepTwoCombobox.setEnabled(True)
                self.ui.sweepTwoMinEdit.setEnabled(True)
                self.ui.sweepTwoMaxEdit.setEnabled(True)
                self.ui.sweepTwoStepsSpinbox.setEnabled(True)

            # Enable file sweep only if checkbox selected
            if self.ui.fileSweepCheckbox.isChecked():
                self.ui.fileSweepAddSpinBox.setEnabled(True)
                self.ui.fileSweepLineEdit.setEnabled(True)
                self.ui.fileSweepMultiplySpinbox.setEnabled(True)
                self.ui.fileSweepOpenPushbutton.setEnabled(True)

            if not self.ui.fileSweepCheckbox.isChecked():
                self.ui.sweepOneCheckbox.setEnabled(True)
            if not self.ui.sweepOneCheckbox.isChecked():
                self.ui.fileSweepCheckbox.setEnabled(True)
        else:
            # Always disable everything
            self.ui.sweepTwoCheckbox.setEnabled(False)
            self.ui.sweepOneCheckbox.setEnabled(False)
            self.ui.fileSweepCheckbox.setEnabled(False)

            self.ui.sweepOneCombobox.setEnabled(False)
            self.ui.sweepOneMinEdit.setEnabled(False)
            self.ui.sweepOneMaxEdit.setEnabled(False)
            self.ui.sweepOneStepsSpinbox.setEnabled(False)

            self.ui.sweepTwoCombobox.setEnabled(False)
            self.ui.sweepTwoMinEdit.setEnabled(False)
            self.ui.sweepTwoMaxEdit.setEnabled(False)
            self.ui.sweepTwoStepsSpinbox.setEnabled(False)

            self.ui.fileSweepAddSpinBox.setEnabled(False)
            self.ui.fileSweepLineEdit.setEnabled(False)
            self.ui.fileSweepMultiplySpinbox.setEnabled(False)
            self.ui.fileSweepOpenPushbutton.setEnabled(False)

    def checkboxOneClicked(self, value):
        if value:
            self.setEnabledOne(True)
            self.ui.sweepTwoCheckbox.setEnabled(True)
            self.ui.fileSweepCheckbox.setEnabled(False)
        else:
            self.setEnabledOne(False)
            self.ui.sweepTwoCheckbox.setEnabled(False)
            self.ui.sweepTwoCheckbox.setChecked(False)
            self.ui.fileSweepCheckbox.setEnabled(True)

    def checkboxTwoClicked(self, value):
        if value:
            self.setEnabledTwo(True)
        else:
            self.setEnabledTwo(False)

    def checkboxFileClicked(self, value):
        if value:
            self.setEnabledFile(True)
            self.ui.sweepOneCheckbox.setEnabled(False)
        else:
            self.setEnabledFile(False)
            self.ui.sweepOneCheckbox.setEnabled(True)

    def comboboxOneChanged(self, text):
        if self.ui.sweepOneCheckbox.isChecked() and self.selectingCallbackEnabled:
            self.setSelectedOne(text)
            self.fillComboboxes()

    def comboboxTwoChanged(self, text):
        if self.ui.sweepTwoCheckbox.isChecked() and self.selectingCallbackEnabled:
            self.setSelectedTwo(text)
            self.fillComboboxes()

    def setSelectedOne(self, identifier):
        self.selectedOneChanged.emit(identifier, self.selectedOne)
        self.selectedOne = identifier

    def setSelectedTwo(self, identifier):
        self.selectedTwoChanged.emit(identifier, self.selectedTwo)
        self.selectedTwo = identifier

    def openFileClicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open profile file", "./profiles/", "CSV UTF-8 (comma delimited)(*.csv)")
        self.ui.fileSweepLineEdit.setText(file_name)
