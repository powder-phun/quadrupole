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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QLabel, QLineEdit, QSizePolicy, QSpinBox,
    QWidget)

class Ui_sweepWidget(object):
    def setupUi(self, sweepWidget):
        if not sweepWidget.objectName():
            sweepWidget.setObjectName(u"sweepWidget")
        sweepWidget.resize(444, 300)
        self.sweepGridLayout = QGridLayout(sweepWidget)
        self.sweepGridLayout.setObjectName(u"sweepGridLayout")
        self.sweepOneMinLabel = QLabel(sweepWidget)
        self.sweepOneMinLabel.setObjectName(u"sweepOneMinLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sweepOneMinLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneMinLabel.setSizePolicy(sizePolicy)
        self.sweepOneMinLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneMinLabel, 0, 4, 1, 1)

        self.sweepTwoStepsSpinbox = QSpinBox(sweepWidget)
        self.sweepTwoStepsSpinbox.setObjectName(u"sweepTwoStepsSpinbox")
        self.sweepTwoStepsSpinbox.setEnabled(False)
        self.sweepTwoStepsSpinbox.setMinimum(2)
        self.sweepTwoStepsSpinbox.setMaximum(100000)

        self.sweepGridLayout.addWidget(self.sweepTwoStepsSpinbox, 1, 10, 1, 1)

        self.sweepTwoCheckbox = QCheckBox(sweepWidget)
        self.sweepTwoCheckbox.setObjectName(u"sweepTwoCheckbox")
        self.sweepTwoCheckbox.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sweepTwoCheckbox.sizePolicy().hasHeightForWidth())
        self.sweepTwoCheckbox.setSizePolicy(sizePolicy1)

        self.sweepGridLayout.addWidget(self.sweepTwoCheckbox, 1, 0, 1, 1)

        self.sweepOneStepsSpinbox = QSpinBox(sweepWidget)
        self.sweepOneStepsSpinbox.setObjectName(u"sweepOneStepsSpinbox")
        self.sweepOneStepsSpinbox.setEnabled(False)
        self.sweepOneStepsSpinbox.setMinimum(2)
        self.sweepOneStepsSpinbox.setMaximum(100000)

        self.sweepGridLayout.addWidget(self.sweepOneStepsSpinbox, 0, 10, 1, 1)

        self.sweepTwoStepsLabel = QLabel(sweepWidget)
        self.sweepTwoStepsLabel.setObjectName(u"sweepTwoStepsLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoStepsLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoStepsLabel.setSizePolicy(sizePolicy)
        self.sweepTwoStepsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoStepsLabel, 1, 9, 1, 1)

        self.sweepTwoLabel = QLabel(sweepWidget)
        self.sweepTwoLabel.setObjectName(u"sweepTwoLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoLabel.setSizePolicy(sizePolicy)
        self.sweepTwoLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoLabel, 1, 2, 1, 1)

        self.sweepOneMaxEdit = QLineEdit(sweepWidget)
        self.sweepOneMaxEdit.setObjectName(u"sweepOneMaxEdit")
        self.sweepOneMaxEdit.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepOneMaxEdit, 0, 8, 1, 1)

        self.sweepOneStepsLabel = QLabel(sweepWidget)
        self.sweepOneStepsLabel.setObjectName(u"sweepOneStepsLabel")
        sizePolicy.setHeightForWidth(self.sweepOneStepsLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneStepsLabel.setSizePolicy(sizePolicy)
        self.sweepOneStepsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneStepsLabel, 0, 9, 1, 1)

        self.sweepTwoMinEdit = QLineEdit(sweepWidget)
        self.sweepTwoMinEdit.setObjectName(u"sweepTwoMinEdit")
        self.sweepTwoMinEdit.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepTwoMinEdit, 1, 5, 1, 1)

        self.sweepOneCombobox = QComboBox(sweepWidget)
        self.sweepOneCombobox.setObjectName(u"sweepOneCombobox")
        self.sweepOneCombobox.setEnabled(False)
        self.sweepOneCombobox.setEditable(False)

        self.sweepGridLayout.addWidget(self.sweepOneCombobox, 0, 3, 1, 1)

        self.sweepOneMinEdit = QLineEdit(sweepWidget)
        self.sweepOneMinEdit.setObjectName(u"sweepOneMinEdit")
        self.sweepOneMinEdit.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepOneMinEdit, 0, 5, 1, 1)

        self.sweepOneLabel = QLabel(sweepWidget)
        self.sweepOneLabel.setObjectName(u"sweepOneLabel")
        sizePolicy.setHeightForWidth(self.sweepOneLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneLabel.setSizePolicy(sizePolicy)
        self.sweepOneLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneLabel, 0, 2, 1, 1)

        self.sweepTwoMinLabel = QLabel(sweepWidget)
        self.sweepTwoMinLabel.setObjectName(u"sweepTwoMinLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoMinLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoMinLabel.setSizePolicy(sizePolicy)
        self.sweepTwoMinLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoMinLabel, 1, 4, 1, 1)

        self.sweepOneCheckbox = QCheckBox(sweepWidget)
        self.sweepOneCheckbox.setObjectName(u"sweepOneCheckbox")
        self.sweepOneCheckbox.setCheckable(True)
        self.sweepOneCheckbox.setChecked(False)

        self.sweepGridLayout.addWidget(self.sweepOneCheckbox, 0, 0, 1, 1)

        self.sweepTwoMaxLabel = QLabel(sweepWidget)
        self.sweepTwoMaxLabel.setObjectName(u"sweepTwoMaxLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoMaxLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoMaxLabel.setSizePolicy(sizePolicy)
        self.sweepTwoMaxLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoMaxLabel, 1, 6, 1, 1)

        self.sweepTwoCombobox = QComboBox(sweepWidget)
        self.sweepTwoCombobox.setObjectName(u"sweepTwoCombobox")
        self.sweepTwoCombobox.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepTwoCombobox, 1, 3, 1, 1)

        self.sweepOneMaxLabel = QLabel(sweepWidget)
        self.sweepOneMaxLabel.setObjectName(u"sweepOneMaxLabel")
        sizePolicy.setHeightForWidth(self.sweepOneMaxLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneMaxLabel.setSizePolicy(sizePolicy)
        self.sweepOneMaxLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneMaxLabel, 0, 6, 1, 1)

        self.sweepTwoMaxEdit = QLineEdit(sweepWidget)
        self.sweepTwoMaxEdit.setObjectName(u"sweepTwoMaxEdit")
        self.sweepTwoMaxEdit.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepTwoMaxEdit, 1, 8, 1, 1)

        QWidget.setTabOrder(self.sweepOneCheckbox, self.sweepOneCombobox)
        QWidget.setTabOrder(self.sweepOneCombobox, self.sweepOneMinEdit)
        QWidget.setTabOrder(self.sweepOneMinEdit, self.sweepOneMaxEdit)
        QWidget.setTabOrder(self.sweepOneMaxEdit, self.sweepOneStepsSpinbox)
        QWidget.setTabOrder(self.sweepOneStepsSpinbox, self.sweepTwoCheckbox)
        QWidget.setTabOrder(self.sweepTwoCheckbox, self.sweepTwoCombobox)
        QWidget.setTabOrder(self.sweepTwoCombobox, self.sweepTwoMinEdit)
        QWidget.setTabOrder(self.sweepTwoMinEdit, self.sweepTwoMaxEdit)
        QWidget.setTabOrder(self.sweepTwoMaxEdit, self.sweepTwoStepsSpinbox)

        self.retranslateUi(sweepWidget)

        self.sweepTwoCombobox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(sweepWidget)
    # setupUi

    def retranslateUi(self, sweepWidget):
        sweepWidget.setWindowTitle(QCoreApplication.translate("sweepWidget", u"Form", None))
        self.sweepOneMinLabel.setText(QCoreApplication.translate("sweepWidget", u"Min:", None))
        self.sweepTwoCheckbox.setText("")
        self.sweepTwoStepsLabel.setText(QCoreApplication.translate("sweepWidget", u"Steps:", None))
        self.sweepTwoLabel.setText(QCoreApplication.translate("sweepWidget", u"Sweep 2:", None))
        self.sweepOneMaxEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
        self.sweepOneStepsLabel.setText(QCoreApplication.translate("sweepWidget", u"Steps:", None))
        self.sweepTwoMinEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
        self.sweepOneCombobox.setCurrentText("")
        self.sweepOneMinEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
        self.sweepOneLabel.setText(QCoreApplication.translate("sweepWidget", u"Sweep 1:", None))
        self.sweepTwoMinLabel.setText(QCoreApplication.translate("sweepWidget", u"Min:", None))
        self.sweepOneCheckbox.setText("")
        self.sweepTwoMaxLabel.setText(QCoreApplication.translate("sweepWidget", u"Max:", None))
        self.sweepOneMaxLabel.setText(QCoreApplication.translate("sweepWidget", u"Max:", None))
        self.sweepTwoMaxEdit.setText(QCoreApplication.translate("sweepWidget", u"0.0", None))
    # retranslateUi

