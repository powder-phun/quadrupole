from PySide6.QtWidgets import QMainWindow, QComboBox
from ui.main_window import Ui_MainWindow

from parameter import ParameterID
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

        # Setting default sweep parameters so that they can be disabled in other menus
        self.sweepOneSelected = self.main.params[0].id
        self.sweepTwoSelected = self.main.params[1].id

        self.fill_comboboxes()
        # Disabling sweep one parameter in paramdock (only sweep one enabled by default)
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
        self.ui.sweepOneCombobox.currentIndexChanged.connect(
            self.combobox_one_index_changed
        )
        self.ui.sweepTwoCombobox.currentIndexChanged.connect(
            self.combobox_two_index_changed
        )

    def set_enabled_sweep_one(self, value):
        # Enabling everything connected with sweep one
        self.ui.sweepOneCombobox.setEnabled(value)
        self.ui.sweepOneMinEdit.setEnabled(value)
        self.ui.sweepOneMaxEdit.setEnabled(value)
        self.ui.sweepOneStepsSpinbox.setEnabled(value)

        # Enabling second sweep checkbox (it cannot be used without first sweep)
        self.ui.sweepTwoCheckbox.setEnabled(value)

        # Reseting second sweep to disabled
        self.ui.sweepTwoCheckbox.setChecked(False)

        # Disabling first sweep parameter in paramdock
        self.ui.paramDock.set_enabled(self.sweepOneSelected, not value)

        # If disabling first sweep disable also the second one
        if not value:
            self.set_enabled_sweep_two(False)
            self.ui.paramDock.set_enabled(self.sweepTwoSelected, True)

    def set_enabled_sweep_two(self, value):
        # Enabling everything connected with sweep two
        self.ui.sweepTwoCombobox.setEnabled(value)
        self.ui.sweepTwoMinEdit.setEnabled(value)
        self.ui.sweepTwoMaxEdit.setEnabled(value)
        self.ui.sweepTwoStepsSpinbox.setEnabled(value)

        # Disabling first sweep parameter in paramdock
        self.ui.paramDock.set_enabled(self.sweepTwoSelected, not value)

    def combobox_one_index_changed(self, value):
        ret = self.process_combobox(
            value,
            self.ui.sweepOneCombobox,
            self.ui.sweepTwoCombobox,
            self.sweepOneSelected,
        )
        if ret is not None:
            self.sweepOneSelected = ret

    def combobox_two_index_changed(self, value):
        ret = self.process_combobox(
            value,
            self.ui.sweepTwoCombobox,
            self.ui.sweepOneCombobox,
            self.sweepTwoSelected,
        )
        if ret is not None:
            self.sweepTwoSelected = ret

    def process_combobox(
        self, value: int, changed: QComboBox, other: QComboBox, previous: ParameterID
    ):
        # Getting selected parameter info
        text = changed.itemText(value)
        identifier = next(param.id for param in self.main.params if param.name == text)

        # Do only if there was a real change of parameter
        if identifier != previous:
            # Disabling sweep parameter in paramdock and restoring previous one
            self.ui.paramDock.set_enabled(identifier, False)
            self.ui.paramDock.set_enabled(previous, True)

            # Removing selected parameter from other sweep combobox and restoring previous one
            other.removeItem(other.findText(text))
            other.addItem(
                next(param.name for param in self.main.params if param.id == previous)
            )

            # Saving selected parameter
            return identifier
        else:
            return None
