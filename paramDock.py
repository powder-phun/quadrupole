from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QLineEdit, QPushButton

from parameter import Parameter, ParameterID

class ParamDock(QWidget):
    def __init__(self, *args, **kwargs):
        super(ParamDock, self).__init__(*args, **kwargs)
        self.verticalLayout = QVBoxLayout()
        self.layout = QGridLayout()
        self.verticalLayout.addLayout(self.layout)
        self.setLayout(self.verticalLayout)
        self.nameLabels = []
        self.valueLabels = []
        self.unitLabels = []
        self.lineEdits = {}
        self.pushButtons = []
       
    def fill(self, params: list[Parameter]):
        for i, param in enumerate(params):
            self.nameLabels.append(QLabel(param.name))
            self.layout.addWidget(self.nameLabels[-1], i, 0)
            self.valueLabels.append(QLabel("0.0"))
            self.layout.addWidget(self.valueLabels[-1], i, 1)
            self.unitLabels.append(QLabel(f"[{param.unit}]"))
            self.layout.addWidget(self.unitLabels[-1], i, 2)

            self.lineEdits[param.id] = QLineEdit()
            self.layout.addWidget(self.lineEdits[param.id], i, 3)
            self.pushButtons.append(QPushButton("Set"))
            self.layout.addWidget(self.pushButtons[-1], i, 4)

            if not param.editable:
                self.lineEdits[param.id].setEnabled(False)
                self.pushButtons[-1].setEnabled(False)
            else:
                self.pushButtons[-1].clicked.connect((lambda identifier: lambda _: self.setValue(identifier))(param.id))

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

    def setValue(self, id: ParameterID):
        print(self.lineEdits[id].text())