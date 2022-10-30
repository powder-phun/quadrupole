from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal

from config import ParamConfig
from utils import FLOAT_VALIDATOR


class ParamDock(QWidget):
    valueSet = Signal(str, float)

    def __init__(self, *args, **kwargs):
        super(ParamDock, self).__init__(*args, **kwargs)
        self.verticalLayout = QVBoxLayout()
        self.layoutEditable = QGridLayout()
        self.layoutNotEditable = QGridLayout()
        self.setLayout(self.verticalLayout)
        self.nameLabels: dict[str, QLabel] = {}
        self.valueLabels: dict[str, QLabel] = {}
        self.unitLabels: dict[str, QLabel] = {}
        self.lineEdits: dict[str, QLineEdit] = {}
        self.pushButtons: dict[str, QPushButton] = {}
        self.params: dict[str, ParamConfig] = {}

    # Generate UI based on list of parameters
    def fill(self, params: dict[str, ParamConfig]):
        self.params = params
        for i, param in enumerate(params.values()):

            self.nameLabels[param.name] = QLabel(f"{param.name}:")
            self.nameLabels[param.name].setAlignment(Qt.AlignRight)

            self.valueLabels[param.name] = QLabel("0.00E+00")
            self.valueLabels[param.name].setAlignment(Qt.AlignRight)

            self.unitLabels[param.name] = QLabel(f"[{param.unit}]")
            self.unitLabels[param.name].setAlignment(Qt.AlignLeft)

            if param.editable:
                # Add to editable table and add lineedit and button
                self.layoutEditable.addWidget(self.nameLabels[param.name], i, 0)
                self.layoutEditable.addWidget(self.valueLabels[param.name], i, 1)
                self.layoutEditable.addWidget(self.unitLabels[param.name], i, 2)

                self.lineEdits[param.name] = QLineEdit()
                self.lineEdits[param.name].setValidator(FLOAT_VALIDATOR)
                self.lineEdits[param.name].setFixedWidth(100)
                self.lineEdits[param.name].setText(str(param.default))
                self.layoutEditable.addWidget(self.lineEdits[param.name], i, 3)
                self.pushButtons[param.name] = QPushButton("Set")
                self.pushButtons[param.name].setFixedWidth(50)
                self.layoutEditable.addWidget(self.pushButtons[param.name], i, 4)

                # Weird lambda to capture id
                self.pushButtons[param.name].clicked.connect(
                    (lambda identifier: lambda _: self.setValue(identifier))(param.name)
                )
                self.lineEdits[param.name].returnPressed.connect(
                    (lambda identifier: lambda: self.setValue(identifier))(param.name)
                )

            else:
                # Add to non editable table
                self.layoutNotEditable.addWidget(self.nameLabels[param.name], i, 0)
                self.layoutNotEditable.addWidget(self.valueLabels[param.name], i, 1)
                self.layoutNotEditable.addWidget(self.unitLabels[param.name], i, 2)

        # Add editable table
        self.verticalLayout.addLayout(self.layoutEditable)
        # Add spacer
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(self.verticalSpacer)
        # Add not editable table
        self.verticalLayout.addLayout(self.layoutNotEditable)

    # Callback for set buttons
    def setValue(self, identifier: str):
        val = (
            float(self.lineEdits[identifier].text())
            if self.lineEdits[identifier].text() != ""
            else 0.0
        )
        self.valueSet.emit(identifier, val)

    def setData(self, identifier, value):
        self.valueLabels[identifier].setText("{:.2E}".format(value))

    # Enabling or disabling editing
    def setEnabledParam(self, name: str, value: bool):
        self.lineEdits[name].setEnabled(value)
        self.pushButtons[name].setEnabled(value)
