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

from parameter import Parameter, ParameterID
from utils import FLOAT_VALIDATOR


class ParamDock(QWidget):
    valueSet = Signal(ParameterID, float)

    def __init__(self, *args, **kwargs):
        super(ParamDock, self).__init__(*args, **kwargs)
        self.verticalLayout = QVBoxLayout()
        self.layoutEditable = QGridLayout()
        self.layoutNotEditable = QGridLayout()
        self.setLayout(self.verticalLayout)
        self.nameLabels: dict[ParameterID, QLabel] = {}
        self.valueLabels: dict[ParameterID, QLabel] = {}
        self.unitLabels: dict[ParameterID, QLabel] = {}
        self.lineEdits: dict[ParameterID, QLineEdit] = {}
        self.pushButtons: dict[ParameterID, QPushButton] = {}

    # Generate UI based on list of parameters
    def fill(self, params: dict[ParameterID, Parameter]):
        for i, param in enumerate(params.values()):

            self.nameLabels[param.id] = QLabel(f"{param.name}:")
            self.nameLabels[param.id].setAlignment(Qt.AlignRight)

            self.valueLabels[param.id] = QLabel("0.0")
            self.valueLabels[param.id].setAlignment(Qt.AlignRight)

            self.unitLabels[param.id] = QLabel(f"[{param.unit}]")
            self.unitLabels[param.id].setAlignment(Qt.AlignLeft)

            if param.editable:
                # Add to editable table and add lineedit and button
                self.layoutEditable.addWidget(self.nameLabels[param.id], i, 0)
                self.layoutEditable.addWidget(self.valueLabels[param.id], i, 1)
                self.layoutEditable.addWidget(self.unitLabels[param.id], i, 2)

                self.lineEdits[param.id] = QLineEdit()
                self.lineEdits[param.id].setValidator(FLOAT_VALIDATOR)
                self.lineEdits[param.id].setFixedWidth(100)
                self.layoutEditable.addWidget(self.lineEdits[param.id], i, 3)
                self.pushButtons[param.id] = QPushButton("Set")
                self.pushButtons[param.id].setFixedWidth(50)
                self.layoutEditable.addWidget(self.pushButtons[param.id], i, 4)

                # Weird lambda to capture id
                self.pushButtons[param.id].clicked.connect(
                    (lambda identifier: lambda _: self.setValue(identifier))(param.id)
                )
                self.lineEdits[param.id].returnPressed.connect(
                    (lambda identifier: lambda: self.setValue(identifier))(param.id)
                )

            else:
                # Add to non editable table
                self.layoutNotEditable.addWidget(self.nameLabels[param.id], i, 0)
                self.layoutNotEditable.addWidget(self.valueLabels[param.id], i, 1)
                self.layoutNotEditable.addWidget(self.unitLabels[param.id], i, 2)

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
    def setValue(self, identifier: ParameterID):
        val = (
            float(self.lineEdits[identifier].text())
            if self.lineEdits[identifier].text() != ""
            else 0.0
        )
        self.valueSet.emit(identifier, val)

    def setData(self, identifier, value):
        self.valueLabels[identifier].setText("{:.2E}".format(value))

    # Enabling or disabling editing
    def setEnabledParam(self, id: ParameterID, value: bool):
        self.lineEdits[id].setEnabled(value)
        self.pushButtons[id].setEnabled(value)
