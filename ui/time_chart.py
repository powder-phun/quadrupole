# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_chart.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_timeChart(object):
    def setupUi(self, timeChart):
        if not timeChart.objectName():
            timeChart.setObjectName(u"timeChart")
        timeChart.resize(1102, 618)
        self.horizontalLayout = QHBoxLayout(timeChart)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.chart = QWidget(timeChart)
        self.chart.setObjectName(u"chart")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chart.sizePolicy().hasHeightForWidth())
        self.chart.setSizePolicy(sizePolicy)

        self.verticalLayout_3.addWidget(self.chart)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.maxYEdit = QLineEdit(timeChart)
        self.maxYEdit.setObjectName(u"maxYEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.maxYEdit.sizePolicy().hasHeightForWidth())
        self.maxYEdit.setSizePolicy(sizePolicy1)
        self.maxYEdit.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_2.addWidget(self.maxYEdit)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.minYEdit = QLineEdit(timeChart)
        self.minYEdit.setObjectName(u"minYEdit")
        sizePolicy1.setHeightForWidth(self.minYEdit.sizePolicy().hasHeightForWidth())
        self.minYEdit.setSizePolicy(sizePolicy1)
        self.minYEdit.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.minYEdit)

        self.minXEdit = QLineEdit(timeChart)
        self.minXEdit.setObjectName(u"minXEdit")
        sizePolicy1.setHeightForWidth(self.minXEdit.sizePolicy().hasHeightForWidth())
        self.minXEdit.setSizePolicy(sizePolicy1)
        self.minXEdit.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.minXEdit)

        self.label = QLabel(timeChart)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.xLabel = QLabel(timeChart)
        self.xLabel.setObjectName(u"xLabel")

        self.horizontalLayout_3.addWidget(self.xLabel)

        self.label_3 = QLabel(timeChart)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.yLabel = QLabel(timeChart)
        self.yLabel.setObjectName(u"yLabel")

        self.horizontalLayout_3.addWidget(self.yLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.maxXEdit = QLineEdit(timeChart)
        self.maxXEdit.setObjectName(u"maxXEdit")
        sizePolicy1.setHeightForWidth(self.maxXEdit.sizePolicy().hasHeightForWidth())
        self.maxXEdit.setSizePolicy(sizePolicy1)
        self.maxXEdit.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.maxXEdit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

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

        self.scaleXCheckbox = QCheckBox(self.widget)
        self.scaleXCheckbox.setObjectName(u"scaleXCheckbox")
        self.scaleXCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scaleXCheckbox)

        self.scaleYCheckbox = QCheckBox(self.widget)
        self.scaleYCheckbox.setObjectName(u"scaleYCheckbox")
        self.scaleYCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scaleYCheckbox)

        self.resetButton = QPushButton(self.widget)
        self.resetButton.setObjectName(u"resetButton")

        self.rightVLayout.addWidget(self.resetButton)

        self.logXAxisCheckbox = QCheckBox(self.widget)
        self.logXAxisCheckbox.setObjectName(u"logXAxisCheckbox")

        self.rightVLayout.addWidget(self.logXAxisCheckbox)

        self.logYAxisCheckbox = QCheckBox(self.widget)
        self.logYAxisCheckbox.setObjectName(u"logYAxisCheckbox")

        self.rightVLayout.addWidget(self.logYAxisCheckbox)


        self.verticalLayout_2.addLayout(self.rightVLayout)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(timeChart)

        QMetaObject.connectSlotsByName(timeChart)
    # setupUi

    def retranslateUi(self, timeChart):
        timeChart.setWindowTitle(QCoreApplication.translate("timeChart", u"Form", None))
        self.maxYEdit.setText("")
        self.label.setText(QCoreApplication.translate("timeChart", u"X:", None))
        self.xLabel.setText(QCoreApplication.translate("timeChart", u"0.0", None))
        self.label_3.setText(QCoreApplication.translate("timeChart", u"Y:", None))
        self.yLabel.setText(QCoreApplication.translate("timeChart", u"0.0", None))
        self.scrollCheckbox.setText(QCoreApplication.translate("timeChart", u"Scroll", None))
        self.scaleXCheckbox.setText(QCoreApplication.translate("timeChart", u"AutoScale X", None))
        self.scaleYCheckbox.setText(QCoreApplication.translate("timeChart", u"AutoScale Y", None))
        self.resetButton.setText(QCoreApplication.translate("timeChart", u"Reset", None))
        self.logXAxisCheckbox.setText(QCoreApplication.translate("timeChart", u"Log X Axis", None))
        self.logYAxisCheckbox.setText(QCoreApplication.translate("timeChart", u"Log Y Axis", None))
    # retranslateUi

