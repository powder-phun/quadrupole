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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

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
        self.chart = QWidget(threeDChart)
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
        self.maxYEdit = QLineEdit(threeDChart)
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
        self.minYEdit = QLineEdit(threeDChart)
        self.minYEdit.setObjectName(u"minYEdit")
        sizePolicy1.setHeightForWidth(self.minYEdit.sizePolicy().hasHeightForWidth())
        self.minYEdit.setSizePolicy(sizePolicy1)
        self.minYEdit.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.minYEdit)

        self.minXEdit = QLineEdit(threeDChart)
        self.minXEdit.setObjectName(u"minXEdit")
        sizePolicy1.setHeightForWidth(self.minXEdit.sizePolicy().hasHeightForWidth())
        self.minXEdit.setSizePolicy(sizePolicy1)
        self.minXEdit.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.minXEdit)

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

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.maxXEdit = QLineEdit(threeDChart)
        self.maxXEdit.setObjectName(u"maxXEdit")
        sizePolicy1.setHeightForWidth(self.maxXEdit.sizePolicy().hasHeightForWidth())
        self.maxXEdit.setSizePolicy(sizePolicy1)
        self.maxXEdit.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.maxXEdit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.widget = QWidget(threeDChart)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rightVLayout = QVBoxLayout()
        self.rightVLayout.setObjectName(u"rightVLayout")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.rightVLayout.addWidget(self.label_2)

        self.xAxisCombobox = QComboBox(self.widget)
        self.xAxisCombobox.setObjectName(u"xAxisCombobox")

        self.rightVLayout.addWidget(self.xAxisCombobox)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.rightVLayout.addWidget(self.label_5)

        self.yAxisCombobox = QComboBox(self.widget)
        self.yAxisCombobox.setObjectName(u"yAxisCombobox")

        self.rightVLayout.addWidget(self.yAxisCombobox)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.rightVLayout.addWidget(self.label_6)

        self.zAxisCombobox = QComboBox(self.widget)
        self.zAxisCombobox.setObjectName(u"zAxisCombobox")

        self.rightVLayout.addWidget(self.zAxisCombobox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.rightVLayout.addItem(self.verticalSpacer)

        self.scaleXCheckbox = QCheckBox(self.widget)
        self.scaleXCheckbox.setObjectName(u"scaleXCheckbox")
        self.scaleXCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scaleXCheckbox)

        self.scaleYCheckbox = QCheckBox(self.widget)
        self.scaleYCheckbox.setObjectName(u"scaleYCheckbox")
        self.scaleYCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scaleYCheckbox)

        self.scaleZCheckbox = QCheckBox(self.widget)
        self.scaleZCheckbox.setObjectName(u"scaleZCheckbox")
        self.scaleZCheckbox.setChecked(True)

        self.rightVLayout.addWidget(self.scaleZCheckbox)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.rightVLayout.addWidget(self.label_4)

        self.zMaxSpinbox = QDoubleSpinBox(self.widget)
        self.zMaxSpinbox.setObjectName(u"zMaxSpinbox")

        self.rightVLayout.addWidget(self.zMaxSpinbox)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.rightVLayout.addWidget(self.label_7)

        self.zMinSpinbox = QDoubleSpinBox(self.widget)
        self.zMinSpinbox.setObjectName(u"zMinSpinbox")

        self.rightVLayout.addWidget(self.zMinSpinbox)

        self.resetButton = QPushButton(self.widget)
        self.resetButton.setObjectName(u"resetButton")

        self.rightVLayout.addWidget(self.resetButton)


        self.verticalLayout_2.addLayout(self.rightVLayout)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(threeDChart)

        QMetaObject.connectSlotsByName(threeDChart)
    # setupUi

    def retranslateUi(self, threeDChart):
        threeDChart.setWindowTitle(QCoreApplication.translate("threeDChart", u"Form", None))
        self.maxYEdit.setText("")
        self.label.setText(QCoreApplication.translate("threeDChart", u"X:", None))
        self.xLabel.setText(QCoreApplication.translate("threeDChart", u"0.0", None))
        self.label_3.setText(QCoreApplication.translate("threeDChart", u"Y:", None))
        self.yLabel.setText(QCoreApplication.translate("threeDChart", u"0.0", None))
        self.label_2.setText(QCoreApplication.translate("threeDChart", u"X Axis:", None))
        self.label_5.setText(QCoreApplication.translate("threeDChart", u"Y Axis:", None))
        self.label_6.setText(QCoreApplication.translate("threeDChart", u"Z Axis:", None))
        self.scaleXCheckbox.setText(QCoreApplication.translate("threeDChart", u"Scale X", None))
        self.scaleYCheckbox.setText(QCoreApplication.translate("threeDChart", u"Scale Y", None))
        self.scaleZCheckbox.setText(QCoreApplication.translate("threeDChart", u"Scale Z", None))
        self.label_4.setText(QCoreApplication.translate("threeDChart", u"Z Max:", None))
        self.label_7.setText(QCoreApplication.translate("threeDChart", u"Z Min:", None))
        self.resetButton.setText(QCoreApplication.translate("threeDChart", u"Reset", None))
    # retranslateUi

