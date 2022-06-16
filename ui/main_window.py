# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDockWidget,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

from paramDock import ParamDock

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1023, 726)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.timeTab = QWidget()
        self.timeTab.setObjectName(u"timeTab")
        self.verticalLayout_2 = QVBoxLayout(self.timeTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plotLayout = QHBoxLayout()
        self.plotLayout.setObjectName(u"plotLayout")
        self.widget = QWidget(self.timeTab)
        self.widget.setObjectName(u"widget")

        self.plotLayout.addWidget(self.widget)


        self.verticalLayout_2.addLayout(self.plotLayout)

        self.verticalLayout_2.setStretch(0, 2)
        self.tabWidget.addTab(self.timeTab, "")
        self.twoDTab = QWidget()
        self.twoDTab.setObjectName(u"twoDTab")
        self.tabWidget.addTab(self.twoDTab, "")
        self.threeDTab = QWidget()
        self.threeDTab.setObjectName(u"threeDTab")
        self.tabWidget.addTab(self.threeDTab, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.settingsHorizontalLayout = QHBoxLayout()
        self.settingsHorizontalLayout.setObjectName(u"settingsHorizontalLayout")
        self.settingsLeftVerticalLayout = QVBoxLayout()
        self.settingsLeftVerticalLayout.setObjectName(u"settingsLeftVerticalLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.settingsLeftVerticalLayout.addWidget(self.titleLabel)

        self.titleEdit = QLineEdit(self.centralwidget)
        self.titleEdit.setObjectName(u"titleEdit")

        self.settingsLeftVerticalLayout.addWidget(self.titleEdit)

        self.commentLabel = QLabel(self.centralwidget)
        self.commentLabel.setObjectName(u"commentLabel")

        self.settingsLeftVerticalLayout.addWidget(self.commentLabel)

        self.commentEdit = QTextEdit(self.centralwidget)
        self.commentEdit.setObjectName(u"commentEdit")

        self.settingsLeftVerticalLayout.addWidget(self.commentEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.settingsLeftVerticalLayout.addItem(self.verticalSpacer)


        self.settingsHorizontalLayout.addLayout(self.settingsLeftVerticalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.settingsHorizontalLayout.addWidget(self.line)

        self.settingsRightVerticalLayout = QVBoxLayout()
        self.settingsRightVerticalLayout.setObjectName(u"settingsRightVerticalLayout")
        self.sweepGridLayout = QGridLayout()
        self.sweepGridLayout.setObjectName(u"sweepGridLayout")
        self.sweepOneMinLabel = QLabel(self.centralwidget)
        self.sweepOneMinLabel.setObjectName(u"sweepOneMinLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sweepOneMinLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneMinLabel.setSizePolicy(sizePolicy)
        self.sweepOneMinLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneMinLabel, 0, 4, 1, 1)

        self.sweepTwoStepsSpinbox = QSpinBox(self.centralwidget)
        self.sweepTwoStepsSpinbox.setObjectName(u"sweepTwoStepsSpinbox")
        self.sweepTwoStepsSpinbox.setEnabled(False)
        self.sweepTwoStepsSpinbox.setMinimum(1)
        self.sweepTwoStepsSpinbox.setMaximum(1000)

        self.sweepGridLayout.addWidget(self.sweepTwoStepsSpinbox, 1, 10, 1, 1)

        self.sweepTwoCheckbox = QCheckBox(self.centralwidget)
        self.sweepTwoCheckbox.setObjectName(u"sweepTwoCheckbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sweepTwoCheckbox.sizePolicy().hasHeightForWidth())
        self.sweepTwoCheckbox.setSizePolicy(sizePolicy1)

        self.sweepGridLayout.addWidget(self.sweepTwoCheckbox, 1, 0, 1, 1)

        self.sweepOneStepsSpinbox = QSpinBox(self.centralwidget)
        self.sweepOneStepsSpinbox.setObjectName(u"sweepOneStepsSpinbox")
        self.sweepOneStepsSpinbox.setMinimum(1)
        self.sweepOneStepsSpinbox.setMaximum(1000)

        self.sweepGridLayout.addWidget(self.sweepOneStepsSpinbox, 0, 10, 1, 1)

        self.sweepTwoStepsLabel = QLabel(self.centralwidget)
        self.sweepTwoStepsLabel.setObjectName(u"sweepTwoStepsLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoStepsLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoStepsLabel.setSizePolicy(sizePolicy)
        self.sweepTwoStepsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoStepsLabel, 1, 9, 1, 1)

        self.sweepTwoLabel = QLabel(self.centralwidget)
        self.sweepTwoLabel.setObjectName(u"sweepTwoLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoLabel.setSizePolicy(sizePolicy)
        self.sweepTwoLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoLabel, 1, 2, 1, 1)

        self.sweepOneMaxEdit = QLineEdit(self.centralwidget)
        self.sweepOneMaxEdit.setObjectName(u"sweepOneMaxEdit")

        self.sweepGridLayout.addWidget(self.sweepOneMaxEdit, 0, 8, 1, 1)

        self.sweepOneStepsLabel = QLabel(self.centralwidget)
        self.sweepOneStepsLabel.setObjectName(u"sweepOneStepsLabel")
        sizePolicy.setHeightForWidth(self.sweepOneStepsLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneStepsLabel.setSizePolicy(sizePolicy)
        self.sweepOneStepsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneStepsLabel, 0, 9, 1, 1)

        self.sweepTwoMinEdit = QLineEdit(self.centralwidget)
        self.sweepTwoMinEdit.setObjectName(u"sweepTwoMinEdit")
        self.sweepTwoMinEdit.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepTwoMinEdit, 1, 5, 1, 1)

        self.sweepOneCombobox = QComboBox(self.centralwidget)
        self.sweepOneCombobox.setObjectName(u"sweepOneCombobox")
        self.sweepOneCombobox.setEditable(False)

        self.sweepGridLayout.addWidget(self.sweepOneCombobox, 0, 3, 1, 1)

        self.sweepOneMinEdit = QLineEdit(self.centralwidget)
        self.sweepOneMinEdit.setObjectName(u"sweepOneMinEdit")

        self.sweepGridLayout.addWidget(self.sweepOneMinEdit, 0, 5, 1, 1)

        self.sweepOneLabel = QLabel(self.centralwidget)
        self.sweepOneLabel.setObjectName(u"sweepOneLabel")
        sizePolicy.setHeightForWidth(self.sweepOneLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneLabel.setSizePolicy(sizePolicy)
        self.sweepOneLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneLabel, 0, 2, 1, 1)

        self.sweepTwoMinLabel = QLabel(self.centralwidget)
        self.sweepTwoMinLabel.setObjectName(u"sweepTwoMinLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoMinLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoMinLabel.setSizePolicy(sizePolicy)
        self.sweepTwoMinLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoMinLabel, 1, 4, 1, 1)

        self.sweepOneCheckbox = QCheckBox(self.centralwidget)
        self.sweepOneCheckbox.setObjectName(u"sweepOneCheckbox")
        self.sweepOneCheckbox.setChecked(True)

        self.sweepGridLayout.addWidget(self.sweepOneCheckbox, 0, 0, 1, 1)

        self.sweepTwoMaxLabel = QLabel(self.centralwidget)
        self.sweepTwoMaxLabel.setObjectName(u"sweepTwoMaxLabel")
        sizePolicy.setHeightForWidth(self.sweepTwoMaxLabel.sizePolicy().hasHeightForWidth())
        self.sweepTwoMaxLabel.setSizePolicy(sizePolicy)
        self.sweepTwoMaxLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepTwoMaxLabel, 1, 6, 1, 1)

        self.sweepTwoCombobox = QComboBox(self.centralwidget)
        self.sweepTwoCombobox.setObjectName(u"sweepTwoCombobox")
        self.sweepTwoCombobox.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepTwoCombobox, 1, 3, 1, 1)

        self.sweepOneMaxLabel = QLabel(self.centralwidget)
        self.sweepOneMaxLabel.setObjectName(u"sweepOneMaxLabel")
        sizePolicy.setHeightForWidth(self.sweepOneMaxLabel.sizePolicy().hasHeightForWidth())
        self.sweepOneMaxLabel.setSizePolicy(sizePolicy)
        self.sweepOneMaxLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.sweepGridLayout.addWidget(self.sweepOneMaxLabel, 0, 6, 1, 1)

        self.sweepTwoMaxEdit = QLineEdit(self.centralwidget)
        self.sweepTwoMaxEdit.setObjectName(u"sweepTwoMaxEdit")
        self.sweepTwoMaxEdit.setEnabled(False)

        self.sweepGridLayout.addWidget(self.sweepTwoMaxEdit, 1, 8, 1, 1)


        self.settingsRightVerticalLayout.addLayout(self.sweepGridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.settingsRightVerticalLayout.addItem(self.verticalSpacer_2)

        self.progressHorizontalLayout = QHBoxLayout()
        self.progressHorizontalLayout.setObjectName(u"progressHorizontalLayout")
        self.stepCountTitleLabel = QLabel(self.centralwidget)
        self.stepCountTitleLabel.setObjectName(u"stepCountTitleLabel")
        self.stepCountTitleLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.progressHorizontalLayout.addWidget(self.stepCountTitleLabel)

        self.stepCountLabel = QLabel(self.centralwidget)
        self.stepCountLabel.setObjectName(u"stepCountLabel")

        self.progressHorizontalLayout.addWidget(self.stepCountLabel)

        self.timeLeftTitleLabel = QLabel(self.centralwidget)
        self.timeLeftTitleLabel.setObjectName(u"timeLeftTitleLabel")
        self.timeLeftTitleLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.progressHorizontalLayout.addWidget(self.timeLeftTitleLabel)

        self.timeLeftLabel = QLabel(self.centralwidget)
        self.timeLeftLabel.setObjectName(u"timeLeftLabel")

        self.progressHorizontalLayout.addWidget(self.timeLeftLabel)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy2)
        self.progressBar.setValue(0)

        self.progressHorizontalLayout.addWidget(self.progressBar)


        self.settingsRightVerticalLayout.addLayout(self.progressHorizontalLayout)

        self.buttonHorizontalLayout = QHBoxLayout()
        self.buttonHorizontalLayout.setObjectName(u"buttonHorizontalLayout")
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")

        self.buttonHorizontalLayout.addWidget(self.startButton)

        self.pauseButton = QPushButton(self.centralwidget)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setEnabled(False)

        self.buttonHorizontalLayout.addWidget(self.pauseButton)


        self.settingsRightVerticalLayout.addLayout(self.buttonHorizontalLayout)


        self.settingsHorizontalLayout.addLayout(self.settingsRightVerticalLayout)

        self.settingsHorizontalLayout.setStretch(0, 1)
        self.settingsHorizontalLayout.setStretch(2, 2)

        self.verticalLayout_3.addLayout(self.settingsHorizontalLayout)

        self.verticalLayout_3.setStretch(0, 2)
        self.verticalLayout_3.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.paramDockWidget = QDockWidget(MainWindow)
        self.paramDockWidget.setObjectName(u"paramDockWidget")
        self.paramDockWidget.setFloating(False)
        self.paramDockWidget.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.paramDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.paramDock = ParamDock()
        self.paramDock.setObjectName(u"paramDock")
        self.paramDockWidget.setWidget(self.paramDock)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.paramDockWidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.sweepTwoCombobox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timeTab), QCoreApplication.translate("MainWindow", u"Time", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.twoDTab), QCoreApplication.translate("MainWindow", u"2D", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.threeDTab), QCoreApplication.translate("MainWindow", u"3D", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Title:", None))
        self.commentLabel.setText(QCoreApplication.translate("MainWindow", u"Comment:", None))
        self.sweepOneMinLabel.setText(QCoreApplication.translate("MainWindow", u"Min:", None))
        self.sweepTwoCheckbox.setText("")
        self.sweepTwoStepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps:", None))
        self.sweepTwoLabel.setText(QCoreApplication.translate("MainWindow", u"Sweep 2:", None))
        self.sweepOneStepsLabel.setText(QCoreApplication.translate("MainWindow", u"Steps:", None))
        self.sweepOneCombobox.setCurrentText("")
        self.sweepOneLabel.setText(QCoreApplication.translate("MainWindow", u"Sweep 1:", None))
        self.sweepTwoMinLabel.setText(QCoreApplication.translate("MainWindow", u"Min:", None))
        self.sweepOneCheckbox.setText("")
        self.sweepTwoMaxLabel.setText(QCoreApplication.translate("MainWindow", u"Max:", None))
        self.sweepOneMaxLabel.setText(QCoreApplication.translate("MainWindow", u"Max:", None))
        self.stepCountTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Step count:", None))
        self.stepCountLabel.setText(QCoreApplication.translate("MainWindow", u"--/--", None))
        self.timeLeftTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Time left:", None))
        self.timeLeftLabel.setText(QCoreApplication.translate("MainWindow", u"-:--:--", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pauseButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.paramDockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
    # retranslateUi

