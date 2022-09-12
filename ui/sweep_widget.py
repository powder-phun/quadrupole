# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sweep_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_sweepWidget(object):
    def setupUi(self, sweepWidget):
        if not sweepWidget.objectName():
            sweepWidget.setObjectName(u"sweepWidget")
        sweepWidget.resize(902, 663)
        self.verticalLayout = QVBoxLayout(sweepWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.sweepTwoMaxEdit = QLineEdit(sweepWidget)
        self.sweepTwoMaxEdit.setObjectName(u"sweepTwoMaxEdit")
        self.sweepTwoMaxEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sweepTwoMaxEdit, 1, 6, 1, 1)

        self.sweepOneMinEdit = QLineEdit(sweepWidget)
        self.sweepOneMinEdit.setObjectName(u"sweepOneMinEdit")
        self.sweepOneMinEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sweepOneMinEdit, 0, 4, 1, 1)

        self.sweepTwoCheckbox = QCheckBox(sweepWidget)
        self.sweepTwoCheckbox.setObjectName(u"sweepTwoCheckbox")
        self.sweepTwoCheckbox.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sweepTwoCheckbox.sizePolicy().hasHeightForWidth())
        self.sweepTwoCheckbox.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.sweepTwoCheckbox, 1, 0, 1, 1)

        self.sweepOneMaxEdit = QLineEdit(sweepWidget)
        self.sweepOneMaxEdit.setObjectName(u"sweepOneMaxEdit")
        self.sweepOneMaxEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sweepOneMaxEdit, 0, 6, 1, 1)

        self.sweepTwoMinLabel = QLabel(sweepWidget)
        self.sweepTwoMinLabel.setObjectName(u"sweepTwoMinLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sweepTwoMinLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoMinLabel.setSizePolicy(sizePolicy1)
        self.sweepTwoMinLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepTwoMinLabel, 1, 3, 1, 1)

        self.sweepOneLabel = QLabel(sweepWidget)
        self.sweepOneLabel.setObjectName(u"sweepOneLabel")
        sizePolicy1.setHeightForWidth(self.sweepOneLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneLabel.setSizePolicy(sizePolicy1)
        self.sweepOneLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepOneLabel, 0, 1, 1, 1)

        self.sweepOneCombobox = QComboBox(sweepWidget)
        self.sweepOneCombobox.setObjectName(u"sweepOneCombobox")
        self.sweepOneCombobox.setEnabled(False)
        self.sweepOneCombobox.setEditable(False)

        self.gridLayout.addWidget(self.sweepOneCombobox, 0, 2, 1, 1)

        self.sweepTwoLabel = QLabel(sweepWidget)
        self.sweepTwoLabel.setObjectName(u"sweepTwoLabel")
        sizePolicy1.setHeightForWidth(self.sweepTwoLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoLabel.setSizePolicy(sizePolicy1)
        self.sweepTwoLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepTwoLabel, 1, 1, 1, 1)

        self.sweepOneMaxLabel = QLabel(sweepWidget)
        self.sweepOneMaxLabel.setObjectName(u"sweepOneMaxLabel")
        sizePolicy1.setHeightForWidth(self.sweepOneMaxLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneMaxLabel.setSizePolicy(sizePolicy1)
        self.sweepOneMaxLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepOneMaxLabel, 0, 5, 1, 1)

        self.sweepOneMinLabel = QLabel(sweepWidget)
        self.sweepOneMinLabel.setObjectName(u"sweepOneMinLabel")
        sizePolicy1.setHeightForWidth(self.sweepOneMinLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneMinLabel.setSizePolicy(sizePolicy1)
        self.sweepOneMinLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepOneMinLabel, 0, 3, 1, 1)

        self.sweepOneCheckbox = QCheckBox(sweepWidget)
        self.sweepOneCheckbox.setObjectName(u"sweepOneCheckbox")
        self.sweepOneCheckbox.setCheckable(True)
        self.sweepOneCheckbox.setChecked(False)

        self.gridLayout.addWidget(self.sweepOneCheckbox, 0, 0, 1, 1)

        self.sweepTwoCombobox = QComboBox(sweepWidget)
        self.sweepTwoCombobox.setObjectName(u"sweepTwoCombobox")
        self.sweepTwoCombobox.setEnabled(False)

        self.gridLayout.addWidget(self.sweepTwoCombobox, 1, 2, 1, 1)

        self.sweepTwoMinEdit = QLineEdit(sweepWidget)
        self.sweepTwoMinEdit.setObjectName(u"sweepTwoMinEdit")
        self.sweepTwoMinEdit.setEnabled(False)

        self.gridLayout.addWidget(self.sweepTwoMinEdit, 1, 4, 1, 1)

        self.sweepTwoMaxLabel = QLabel(sweepWidget)
        self.sweepTwoMaxLabel.setObjectName(u"sweepTwoMaxLabel")
        sizePolicy1.setHeightForWidth(self.sweepTwoMaxLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoMaxLabel.setSizePolicy(sizePolicy1)
        self.sweepTwoMaxLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepTwoMaxLabel, 1, 5, 1, 1)

        self.sweepOneStepsLabel = QLabel(sweepWidget)
        self.sweepOneStepsLabel.setObjectName(u"sweepOneStepsLabel")
        sizePolicy1.setHeightForWidth(self.sweepOneStepsLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneStepsLabel.setSizePolicy(sizePolicy1)
        self.sweepOneStepsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepOneStepsLabel, 0, 7, 1, 1)

        self.sweepOneStepsSpinbox = QSpinBox(sweepWidget)
        self.sweepOneStepsSpinbox.setObjectName(u"sweepOneStepsSpinbox")
        self.sweepOneStepsSpinbox.setEnabled(False)
        self.sweepOneStepsSpinbox.setMinimum(2)
        self.sweepOneStepsSpinbox.setMaximum(100000)

        self.gridLayout.addWidget(self.sweepOneStepsSpinbox, 0, 8, 1, 1)

        self.sweepTwoStepsLabel = QLabel(sweepWidget)
        self.sweepTwoStepsLabel.setObjectName(u"sweepTwoStepsLabel")
        sizePolicy1.setHeightForWidth(self.sweepTwoStepsLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoStepsLabel.setSizePolicy(sizePolicy1)
        self.sweepTwoStepsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.sweepTwoStepsLabel, 1, 7, 1, 1)

        self.sweepTwoStepsSpinbox = QSpinBox(sweepWidget)
        self.sweepTwoStepsSpinbox.setObjectName(u"sweepTwoStepsSpinbox")
        self.sweepTwoStepsSpinbox.setEnabled(False)
        self.sweepTwoStepsSpinbox.setMinimum(2)
        self.sweepTwoStepsSpinbox.setMaximum(100000)

        self.gridLayout.addWidget(self.sweepTwoStepsSpinbox, 1, 8, 1, 1)

        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(6, 1)
        self.gridLayout.setColumnStretch(8, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox = QCheckBox(sweepWidget)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)

        self.label = QLabel(sweepWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(sweepWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(sweepWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.label_3 = QLabel(sweepWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.doubleSpinBox = QDoubleSpinBox(sweepWidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")

        self.horizontalLayout.addWidget(self.doubleSpinBox)

        self.label_4 = QLabel(sweepWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.doubleSpinBox_2 = QDoubleSpinBox(sweepWidget)
        self.doubleSpinBox_2.setObjectName(u"doubleSpinBox_2")

        self.horizontalLayout.addWidget(self.doubleSpinBox_2)

        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(5, 1)
        self.horizontalLayout.setStretch(7, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(sweepWidget)

        self.sweepTwoCombobox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(sweepWidget)
    # setupUi

    def retranslateUi(self, sweepWidget):
        sweepWidget.setWindowTitle(QCoreApplication.translate("sweepWidget", u"Form", None))
        self.sweepTwoMaxEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
        self.sweepOneMinEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
        self.sweepTwoCheckbox.setText("")
        self.sweepOneMaxEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
        self.sweepTwoMinLabel.setText(QCoreApplication.translate("sweepWidget", u"Min:", None))
        self.sweepOneLabel.setText(QCoreApplication.translate("sweepWidget", u"Sweep 1:", None))
        self.sweepOneCombobox.setCurrentText("")
        self.sweepTwoLabel.setText(QCoreApplication.translate("sweepWidget", u"Sweep 2:", None))
        self.sweepOneMaxLabel.setText(QCoreApplication.translate("sweepWidget", u"Max:", None))
        self.sweepOneMinLabel.setText(QCoreApplication.translate("sweepWidget", u"Min:", None))
        self.sweepOneCheckbox.setText("")
        self.sweepTwoMinEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
        self.sweepTwoMaxLabel.setText(QCoreApplication.translate("sweepWidget", u"Max:", None))
        self.sweepOneStepsLabel.setText(QCoreApplication.translate("sweepWidget", u"Steps:", None))
        self.sweepTwoStepsLabel.setText(QCoreApplication.translate("sweepWidget", u"Steps:", None))
        self.checkBox.setText("")
        self.label.setText(QCoreApplication.translate("sweepWidget", u"FIle sweep:", None))
        self.pushButton.setText(QCoreApplication.translate("sweepWidget", u"Open", None))
        self.label_3.setText(QCoreApplication.translate("sweepWidget", u"Multiply:", None))
        self.label_4.setText(QCoreApplication.translate("sweepWidget", u"Add:", None))
    # retranslateUi

