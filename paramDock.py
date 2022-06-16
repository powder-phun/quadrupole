from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

from parameter import Parameter, ParameterID
from utils import FLOAT_VALIDATOR


class ParamDock(QWidget):
    def __init__(self, *args, **kwargs):
        super(ParamDock, self).__init__(*args, **kwargs)
        self.verticalLayout = QVBoxLayout()
        self.layoutEditable = QGridLayout()
        self.layoutNotEditable = QGridLayout()
        self.setLayout(self.verticalLayout)
        self.nameLabels = {}
        self.valueLabels = {}
        self.unitLabels = {}
        self.lineEdits = {}
        self.pushButtons = {}
       
    def fill(self, params: list[Parameter]):
        for i, param in enumerate(params):

            self.nameLabels[param.id] = (QLabel(f"{param.name}:"))
            self.nameLabels[param.id].setAlignment(Qt.AlignRight)

            self.valueLabels[param.id] = (QLabel("0.0"))
            self.valueLabels[param.id].setAlignment(Qt.AlignRight)

            self.unitLabels[param.id] = (QLabel(f"[{param.unit}]"))
            self.unitLabels[param.id].setAlignment(Qt.AlignLeft)

            if param.editable:

                self.layoutEditable.addWidget(self.nameLabels[param.id], i, 0)
                self.layoutEditable.addWidget(self.valueLabels[param.id], i, 1)
                self.layoutEditable.addWidget(self.unitLabels[param.id], i, 2)

                self.lineEdits[param.id] = QLineEdit()
                self.lineEdits[param.id].setValidator(FLOAT_VALIDATOR)
                self.layoutEditable.addWidget(self.lineEdits[param.id], i, 3)
                self.pushButtons[param.id] = (QPushButton("Set"))
                self.layoutEditable.addWidget(self.pushButtons[param.id], i, 4)

                self.pushButtons[param.id].clicked.connect((lambda identifier: lambda _: self.set_value(identifier))(param.id))

            else:
                self.layoutNotEditable.addWidget(self.nameLabels[param.id], i, 0)
                self.layoutNotEditable.addWidget(self.valueLabels[param.id], i, 1)
                self.layoutNotEditable.addWidget(self.unitLabels[param.id], i, 2)

        self.verticalLayout.addLayout(self.layoutEditable)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.verticalLayout.addLayout(self.layoutNotEditable)

    def set_value(self, id: ParameterID):
        print(float(self.lineEdits[id].text()))

    def set_enabled(self, id: ParameterID, value: bool):
        self.lineEdits[id].setEnabled(value)
        self.pushButtons[id].setEnabled(value)
