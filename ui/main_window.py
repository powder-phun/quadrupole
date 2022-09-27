# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

from paramDock import ParamDock
from sweepWidget import SweepWidget
from threeDChart import ThreeDChart
from timeChart import TimeChart
from twoDChart import TwoDChart

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
        self.timeChart = TimeChart(self.timeTab)
        self.timeChart.setObjectName(u"timeChart")

        self.verticalLayout_2.addWidget(self.timeChart)

        self.tabWidget.addTab(self.timeTab, "")
        self.twoDTab = QWidget()
        self.twoDTab.setObjectName(u"twoDTab")
        self.verticalLayout = QVBoxLayout(self.twoDTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.twoDChart = TwoDChart(self.twoDTab)
        self.twoDChart.setObjectName(u"twoDChart")

        self.verticalLayout.addWidget(self.twoDChart)

        self.tabWidget.addTab(self.twoDTab, "")
        self.threeDTab = QWidget()
        self.threeDTab.setObjectName(u"threeDTab")
        self.verticalLayout_4 = QVBoxLayout(self.threeDTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.threeDChart = ThreeDChart(self.threeDTab)
        self.threeDChart.setObjectName(u"threeDChart")

        self.verticalLayout_4.addWidget(self.threeDChart)

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
        self.sweepWidget = SweepWidget(self.centralwidget)
        self.sweepWidget.setObjectName(u"sweepWidget")

        self.settingsRightVerticalLayout.addWidget(self.sweepWidget)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.settingsRightVerticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.enableButton = QPushButton(self.centralwidget)
        self.enableButton.setObjectName(u"enableButton")

        self.horizontalLayout_2.addWidget(self.enableButton)


        self.settingsRightVerticalLayout.addLayout(self.horizontalLayout_2)

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
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setValue(0)

        self.progressHorizontalLayout.addWidget(self.progressBar)


        self.settingsRightVerticalLayout.addLayout(self.progressHorizontalLayout)

        self.buttonHorizontalLayout = QHBoxLayout()
        self.buttonHorizontalLayout.setObjectName(u"buttonHorizontalLayout")
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")

        self.buttonHorizontalLayout.addWidget(self.startButton)

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setEnabled(False)

        self.buttonHorizontalLayout.addWidget(self.stopButton)


        self.settingsRightVerticalLayout.addLayout(self.buttonHorizontalLayout)


        self.settingsHorizontalLayout.addLayout(self.settingsRightVerticalLayout)

        self.settingsHorizontalLayout.setStretch(0, 1)
        self.settingsHorizontalLayout.setStretch(2, 3)

        self.verticalLayout_3.addLayout(self.settingsHorizontalLayout)

        self.verticalLayout_3.setStretch(0, 3)
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


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Quadrupole Mass Spectrometer Measurement Software", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timeTab), QCoreApplication.translate("MainWindow", u"Time", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.twoDTab), QCoreApplication.translate("MainWindow", u"2D", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.threeDTab), QCoreApplication.translate("MainWindow", u"3D", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Title:", None))
        self.commentLabel.setText(QCoreApplication.translate("MainWindow", u"Comment:", None))
        self.enableButton.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.stepCountTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Step count:", None))
        self.stepCountLabel.setText(QCoreApplication.translate("MainWindow", u"--/--", None))
        self.timeLeftTitleLabel.setText(QCoreApplication.translate("MainWindow", u"Time left:", None))
        self.timeLeftLabel.setText(QCoreApplication.translate("MainWindow", u"-:--:--", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(shortcut)
        self.startButton.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))
#endif // QT_CONFIG(shortcut)
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.paramDockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
    # retranslateUi

