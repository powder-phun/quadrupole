# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_chart.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_timeChart(object):
    def setupUi(self, timeChart):
        if not timeChart.objectName():
            timeChart.setObjectName(u"timeChart")
        timeChart.resize(1102, 618)
        self.horizontalLayout = QHBoxLayout(timeChart)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.chart = QWidget(timeChart)
        self.chart.setObjectName(u"chart")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chart.sizePolicy().hasHeightForWidth())
        self.chart.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.chart)

        self.widget = QWidget(timeChart)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rightVLayout = QVBoxLayout()
        self.rightVLayout.setObjectName(u"rightVLayout")
        self.checkboxLayout = QVBoxLayout()
        self.checkboxLayout.setObjectName(u"checkboxLayout")

        self.rightVLayout.addLayout(self.checkboxLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.rightVLayout.addItem(self.verticalSpacer)

        self.scrollCheckbox = QCheckBox(self.widget)
        self.scrollCheckbox.setObjectName(u"scrollCheckbox")
        self.scrollCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scrollCheckbox)

        self.scaleCheckbox = QCheckBox(self.widget)
        self.scaleCheckbox.setObjectName(u"scaleCheckbox")
        self.scaleCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scaleCheckbox)

        self.resetButton = QPushButton(self.widget)
        self.resetButton.setObjectName(u"resetButton")

        self.rightVLayout.addWidget(self.resetButton)


        self.verticalLayout_2.addLayout(self.rightVLayout)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(timeChart)

        QMetaObject.connectSlotsByName(timeChart)
    # setupUi

    def retranslateUi(self, timeChart):
        timeChart.setWindowTitle(QCoreApplication.translate("timeChart", u"Form", None))
        self.scrollCheckbox.setText(QCoreApplication.translate("timeChart", u"Scroll", None))
        self.scaleCheckbox.setText(QCoreApplication.translate("timeChart", u"Scale", None))
        self.resetButton.setText(QCoreApplication.translate("timeChart", u"Reset", None))
    # retranslateUi

