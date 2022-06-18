from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from ui.sweep_widget import Ui_sweepWidget
from utils import FLOAT_VALIDATOR
from parameter import ParameterID, Parameter


class SweepWidget(QWidget):
    selectedOneChanged = Signal(ParameterID, ParameterID)
    selectedTwoChanged = Signal(ParameterID, ParameterID)

    def __init__(self, parent=None):
        super(SweepWidget, self).__init__(parent)
        self.ui = Ui_sweepWidget()
        self.ui.setupUi(self)

        self.selectedOne: ParameterID = None
        self.selectedTwo: ParameterID = None

        self.selectingCallbackEnabled = True

        self.params: dict[ParameterId, Parameter] = None

        self.ui.sweepOneMinEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepOneMaxEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepTwoMinEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepTwoMaxEdit.setValidator(FLOAT_VALIDATOR)

        self.connectAll()

    def connectAll(self):
        self.ui.sweepOneCheckbox.stateChanged.connect(self.checkboxOneClicked)
        self.ui.sweepTwoCheckbox.stateChanged.connect(self.checkboxTwoClicked)

        self.ui.sweepOneCombobox.currentTextChanged.connect(self.comboboxOneChanged)
        self.ui.sweepTwoCombobox.currentTextChanged.connect(self.comboboxTwoChanged)

    def fillComboboxes(self):
        # Disable callback on change
        self.selectingCallbackEnabled = False

        # Clear comboboxes from previous
        self.ui.sweepOneCombobox.clear()
        self.ui.sweepTwoCombobox.clear()

        # Fill comboboxes
        for param in self.params.values():
            if param.editable:
                if param.id != self.selectedOne:
                    self.ui.sweepTwoCombobox.addItem(param.name)
                if param.id != self.selectedTwo:
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
            self.setSelectedOne(
                next(
                    param.id
                    for param in self.params.values()
                    if param.name == self.ui.sweepOneCombobox.currentText()
                )
            )
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
            self.setSelectedTwo(
                next(
                    param.id
                    for param in self.params.values()
                    if param.name == self.ui.sweepTwoCombobox.currentText()
                )
            )
        else:
            self.setSelectedTwo(None)

        # Re-setup comboboxes
        self.fillComboboxes()

    def setEnabledEverything(self, value):
        if value:
            # Enable sweep one only if checkbox selected
            if self.ui.sweepOneCheckbox.isChecked():
                self.ui.sweepTwoCheckbox.setEnabled(True)

                self.sweepOneCombobox.setEnabled(True)
                self.sweepOneMinEdit.setEnabled(True)
                self.sweepOneMaxEdit.setEnabled(True)
                self.sweepOneStepsSpinbox.setEnabled(True)

            # Enable sweep two only if checkbox selected
            if self.ui.sweepTwoCheckbox.isChecked():
                self.sweepTwoCombobox.setEnabled(True)
                self.sweepTwoMinEdit.setEnabled(True)
                self.sweepTwoMaxEdit.setEnabled(True)
                self.sweepTwoStepsSpinbox.setEnabled(True)
        else:
            # Always disable everything
            self.ui.sweepTwoCheckbox.setEnabled(False)

            self.sweepOneCombobox.setEnabled(False)
            self.sweepOneMinEdit.setEnabled(False)
            self.sweepOneMaxEdit.setEnabled(False)
            self.sweepOneStepsSpinbox.setEnabled(False)

            self.sweepTwoCombobox.setEnabled(False)
            self.sweepTwoMinEdit.setEnabled(False)
            self.sweepTwoMaxEdit.setEnabled(False)
            self.sweepTwoStepsSpinbox.setEnabled(False)

        self.ui.sweepOneCheckbox.setEnabled(value)

    def checkboxOneClicked(self, value):
        if value:
            self.setEnabledOne(True)
            self.ui.sweepTwoCheckbox.setEnabled(True)
        else:
            self.setEnabledOne(False)
            self.ui.sweepTwoCheckbox.setEnabled(False)
            self.ui.sweepTwoCheckbox.setChecked(False)

    def checkboxTwoClicked(self, value):
        if value:
            self.setEnabledTwo(True)
        else:
            self.setEnabledTwo(False)

    def comboboxOneChanged(self, text):
        if self.ui.sweepOneCheckbox.isChecked() and self.selectingCallbackEnabled:
            identifier = next(
                param.id for param in self.params.values() if param.name == text
            )
            self.setSelectedOne(identifier)
            self.fillComboboxes()

    def comboboxTwoChanged(self, text):
        if self.ui.sweepTwoCheckbox.isChecked() and self.selectingCallbackEnabled:
            identifier = next(
                param.id for param in self.params.values() if param.name == text
            )
            self.setSelectedTwo(identifier)
            self.fillComboboxes()

    def setSelectedOne(self, identifier):
        self.selectedOneChanged.emit(identifier, self.selectedOne)
        self.selectedOne = identifier

    def setSelectedTwo(self, identifier):
        self.selectedTwoChanged.emit(identifier, self.selectedTwo)
        self.selectedTwo = identifier
