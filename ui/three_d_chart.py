# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'three_d_chart.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_threeDChart(object):
    def setupUi(self, threeDChart):
        if not threeDChart.objectName():
            threeDChart.setObjectName(u"threeDChart")
        threeDChart.resize(1102, 618)
        self.horizontalLayout = QHBoxLayout(threeDChart)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.chartLayout = QHBoxLayout()
        self.chartLayout.setObjectName(u"chartLayout")
        self.chartLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.chartLayout.setContentsMargins(-1, -1, -1, 0)
        self.chart = QWidget(threeDChart)
        self.chart.setObjectName(u"chart")

        self.chartLayout.addWidget(self.chart)


        self.verticalLayout_3.addLayout(self.chartLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(threeDChart)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.xLabel = QLabel(threeDChart)
        self.xLabel.setObjectName(u"xLabel")

        self.horizontalLayout_3.addWidget(self.xLabel)

        self.label_3 = QLabel(threeDChart)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.yLabel = QLabel(threeDChart)
        self.yLabel.setObjectName(u"yLabel")

        self.horizontalLayout_3.addWidget(self.yLabel)

        self.label_2 = QLabel(threeDChart)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.zLabel = QLabel(threeDChart)
        self.zLabel.setObjectName(u"zLabel")

        self.horizontalLayout_3.addWidget(self.zLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_3.setStretch(0, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.widget = QWidget(threeDChart)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rightVLayout = QVBoxLayout()
        self.rightVLayout.setObjectName(u"rightVLayout")
        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.rightVLayout.addWidget(self.label_6)

        self.zAxisCombobox = QComboBox(self.widget)
        self.zAxisCombobox.setObjectName(u"zAxisCombobox")

        self.rightVLayout.addWidget(self.zAxisCombobox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.rightVLayout.addItem(self.verticalSpacer)

        self.scaleZCheckbox = QCheckBox(self.widget)
        self.scaleZCheckbox.setObjectName(u"scaleZCheckbox")
        self.scaleZCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scaleZCheckbox)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.rightVLayout.addWidget(self.label_7)

        self.zMinLineEdit = QLineEdit(self.widget)
        self.zMinLineEdit.setObjectName(u"zMinLineEdit")
        self.zMinLineEdit.setEnabled(False)

        self.rightVLayout.addWidget(self.zMinLineEdit)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.rightVLayout.addWidget(self.label_4)

        self.zMaxLineEdit = QLineEdit(self.widget)
        self.zMaxLineEdit.setObjectName(u"zMaxLineEdit")
        self.zMaxLineEdit.setEnabled(False)

        self.rightVLayout.addWidget(self.zMaxLineEdit)


        self.verticalLayout_2.addLayout(self.rightVLayout)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalLayout.setStretch(0, 1)

        self.retranslateUi(threeDChart)

        QMetaObject.connectSlotsByName(threeDChart)
    # setupUi

    def retranslateUi(self, threeDChart):
        threeDChart.setWindowTitle(QCoreApplication.translate("threeDChart", u"Form", None))
        self.label.setText(QCoreApplication.translate("threeDChart", u"X:", None))
        self.xLabel.setText(QCoreApplication.translate("threeDChart", u"0.0", None))
        self.label_3.setText(QCoreApplication.translate("threeDChart", u"Y:", None))
        self.yLabel.setText(QCoreApplication.translate("threeDChart", u"0.0", None))
        self.label_2.setText(QCoreApplication.translate("threeDChart", u"Z:", None))
        self.zLabel.setText(QCoreApplication.translate("threeDChart", u"0.0", None))
        self.label_6.setText(QCoreApplication.translate("threeDChart", u"Z Axis:", None))
        self.scaleZCheckbox.setText(QCoreApplication.translate("threeDChart", u"Scale Z", None))
        self.label_7.setText(QCoreApplication.translate("threeDChart", u"Z Min:", None))
        self.label_4.setText(QCoreApplication.translate("threeDChart", u"Z Max:", None))
    # retranslateUi

