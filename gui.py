from PySide6.QtWidgets import QMainWindow
from ui.main_window import Ui_MainWindow
from utils import FLOAT_VALIDATOR

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.main = None
        self.sweepOneSelected = None
        self.sweepTwoSelected = None
    
    def initialize(self, main):
        self.main = main
        self.ui.paramDock.fill(self.main.params)

        self.ui.sweepOneMinEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepOneMaxEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepTwoMinEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.sweepTwoMaxEdit.setValidator(FLOAT_VALIDATOR)

        self.sweepOneSelected = self.main.params[0].id
        self.sweepTwoSelected = self.main.params[1].id
        self.fill_comboboxes()
        self.ui.paramDock.set_enabled(self.sweepOneSelected, False)

        self.connect_all()

    def fill_comboboxes(self):
        for param in self.main.params:
            if param.editable:
                if param.id != self.sweepTwoSelected:
                    self.ui.sweepOneCombobox.addItem(param.name)
                if param.id != self.sweepOneSelected:
                    self.ui.sweepTwoCombobox.addItem(param.name)

    def connect_all(self):
        self.ui.sweepOneCheckbox.stateChanged.connect(self.set_enabled_sweep_one)
        self.ui.sweepTwoCheckbox.stateChanged.connect(self.set_enabled_sweep_two)
        self.ui.sweepOneCombobox.currentIndexChanged.connect(self.combobox_one_index_changed)
        self.ui.sweepTwoCombobox.currentIndexChanged.connect(self.combobox_two_index_changed)

    def set_enabled_sweep_one(self, value):
        self.ui.sweepOneCombobox.setEnabled(value)
        self.ui.sweepOneMinEdit.setEnabled(value)
        self.ui.sweepOneMaxEdit.setEnabled(value)
        self.ui.sweepOneStepsSpinbox.setEnabled(value)
        self.ui.sweepTwoCheckbox.setEnabled(value)
        self.ui.sweepTwoCheckbox.setChecked(False)
        self.ui.paramDock.set_enabled(self.sweepOneSelected, not value)
        if not value:
            self.set_enabled_sweep_two(False)
            self.ui.paramDock.set_enabled(self.sweepTwoSelected, True)

    def set_enabled_sweep_two(self, value):
        self.ui.sweepTwoCombobox.setEnabled(value)
        self.ui.sweepTwoMinEdit.setEnabled(value)
        self.ui.sweepTwoMaxEdit.setEnabled(value)
        self.ui.sweepTwoStepsSpinbox.setEnabled(value)
        self.ui.paramDock.set_enabled(self.sweepTwoSelected, not value)


    def combobox_one_index_changed(self, value):
        text = self.ui.sweepOneCombobox.itemText(value)
        identifier = next(param.id for param in self.main.params if param.name==text)
        if identifier != self.sweepOneSelected:
            self.ui.paramDock.set_enabled(identifier, False)

            self.ui.sweepTwoCombobox.removeItem(self.ui.sweepTwoCombobox.findText(text))  # Remove parameter from other combobox
            self.ui.sweepTwoCombobox.addItem(next(param.name for param in self.main.params if param.id==self.sweepOneSelected)) # Restore previously removed parameter from other combobox

            self.ui.paramDock.set_enabled(self.sweepOneSelected, True)
            self.sweepOneSelected = identifier
    
    def combobox_two_index_changed(self, value):
        text = self.ui.sweepTwoCombobox.itemText(value)
        identifier = next(param.id for param in self.main.params if param.name==text)
        if identifier != self.sweepTwoSelected:
            self.ui.paramDock.set_enabled(identifier, False)

            self.ui.sweepOneCombobox.removeItem(self.ui.sweepOneCombobox.findText(text))  # Remove parameter from other combobox
            self.ui.sweepOneCombobox.addItem(next(param.name for param in self.main.params if param.id==self.sweepTwoSelected)) # Restore previously removed parameter from other combobox

            self.ui.paramDock.set_enabled(self.sweepTwoSelected, True)
            self.sweepTwoSelected = identifier
