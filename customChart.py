from PySide6.QtWidgets import QWidget, QCheckBox
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QLogValueAxis, QAbstractSeries, QLineSeries
from PySide6.QtCore import Qt, QMargins, Signal, Slot
from PySide6.QtGui import QPainter, QMouseEvent

from ui.time_chart import Ui_timeChart

from config import ParamConfig
from utils import DataPacket, FLOAT_VALIDATOR

import logging


class CustomChart(QWidget):
    def __init__(self, parent=None):
        super(CustomChart, self).__init__(parent)
        self.chart = QChart()
        self.chartView = ModifiedChartView(self.chart)
        self.ui = None
        self.setupUi()

        self.series: dict[str, QLineSeries] = {}

        self.xAxis: QValueAxis = QValueAxis()
        self.yAxis: QValueAxis = QValueAxis()

        self.xMin: float = 0
        self.xMax: float = 1
        self.yMin: float = -1
        self.yMax: float = 1

        self.timestamps: list[float] = []

        self.initialize()

        self.checkboxes: dict[str, QCheckBox] = {}

        self.data: dict[str, list[float]] = {}
        self.params: dict[str, ParamConfig] = None

        self.is_x_log = False
        self.is_y_log = False

    def initialize(self):

        # Visual settings
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.chart.legend().setVisible(False)

        # Axis settings
        self.xAxis.setLabelFormat("%.2e")
        self.yAxis.setLabelFormat("%.2e")

        self.chart.addAxis(self.xAxis, Qt.AlignBottom)
        self.chart.addAxis(self.yAxis, Qt.AlignLeft)

        # Setting zooming by rect
        self.chartView.setRubberBand(QChartView.RectangleRubberBand)

        # Connecting signals
        self.chartView.mouseMoved.connect(self.mouseMoved)
        self.ui.resetButton.clicked.connect(self.resetView)
        self.chartView.viewChanged.connect(self.viewChanged)


    def setup(self, params: dict[str, ParamConfig]):
        self.params = params
        for identifier, param in params.items():

            # Creating a series for each parameter
            self.series[identifier] = self.createSeries()
            self.chart.addSeries(self.series[identifier])
            self.series[identifier].attachAxis(self.xAxis)
            self.series[identifier].setUseOpenGL(True)
            self.series[identifier].attachAxis(self.yAxis)
            self.series[identifier].setName(param.name)
            self.series[identifier].setVisible(False)

            # Creating checkboxes for parameters
            self.checkboxes[identifier] = QCheckBox(param.name)
            self.ui.checkboxLayout.addWidget(self.checkboxes[identifier])
            self.checkboxes[identifier].setStyleSheet(
                "QCheckBox {background-color:"
                + self.series[identifier].color().name()
                + "}"
            )
            # Weird lambda to capture parameter
            self.checkboxes[identifier].clicked.connect(
                (
                    lambda identifier: lambda value: self.checkboxClicked(
                        identifier, value
                    )
                )(identifier)
            )

            self.data[identifier] = []
            

        # Setting lineedits
        self.ui.minXEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.maxXEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.minYEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.maxYEdit.setValidator(FLOAT_VALIDATOR)
        self.ui.minXEdit.editingFinished.connect(self.scaleChanged)
        self.ui.maxXEdit.editingFinished.connect(self.scaleChanged)
        self.ui.minYEdit.editingFinished.connect(self.scaleChanged)
        self.ui.maxYEdit.editingFinished.connect(self.scaleChanged)
        self.ui.logXAxisCheckbox.stateChanged.connect(self.setLogXAxis)
        self.ui.logYAxisCheckbox.stateChanged.connect(self.setLogYAxis)

        logging.debug("Setup complete")

    def createSeries(self) -> QAbstractSeries:
        return QLineSeries()

    def addData(self, packet: DataPacket):

        # Saving timestamps
        self.timestamps.append(packet.timestamp)

        # Adding data
        for identifier, value in packet.data.items():
            if self.is_y_log:
                self.data[identifier].append(abs(value))
            else:
                self.data[identifier].append(value)
        self.updateSeries(packet)

        self.scale()
        
    def checkboxClicked(self, param, value):
        self.series[param].setVisible(value)
        self.scale()

        
    def clear(self):
        for series in self.series.values():
            series.clear()
        for k in self.data.keys():
            self.data[k] = []

        logging.debug("Clearing series and data")


    @Slot(float, float)
    def mouseMoved(self, x: float, y: float):
        self.ui.xLabel.setText("{:.2E}".format(x))
        self.ui.yLabel.setText("{:.2E}".format(y))

    def scaleChanged(self):
        self.xMin = float(self.ui.minXEdit.text())
        self.xMax = float(self.ui.maxXEdit.text())
        self.yMin = float(self.ui.minYEdit.text())
        self.yMax = float(self.ui.maxYEdit.text())

        self.updateXRange()
        self.updateYRange()

    def updateXRange(self):
        xMin = self.xMin
        xMax = self.xMax
        if self.is_x_log:
            xMin = max(self.xMin, 1e-20)
            xMax = max(self.xMax, 1e-18)
        self.xAxis.setRange(xMin, xMax)
        self.ui.minXEdit.setText("{:.2E}".format(xMin))
        self.ui.maxXEdit.setText("{:.2E}".format(xMax))

    def updateYRange(self):
        yMin = self.yMin
        yMax = self.yMax
        if self.is_y_log:
            yMin = max(self.yMin, 1e-20)
            yMax = max(self.yMax, 1e-18)
        self.yAxis.setRange(yMin, yMax)
        self.ui.minYEdit.setText("{:.2E}".format(yMin))
        self.ui.maxYEdit.setText("{:.2E}".format(yMax))

    def viewChanged(self):
        self.xMin = self.xAxis.min()
        self.xMax = self.xAxis.max()
        self.updateXRange()

        self.yMin = self.yAxis.min()
        self.yMax = self.yAxis.max()
        self.updateYRange()

    def resetView(self):
        self.scale(True)

    def setLogXAxis(self, is_log=True):
        self.is_x_log = is_log
        logging.debug(f'Setting x axis to {"log" if is_log else "linear"}')

        for series in self.series.values():
            series.detachAxis(self.xAxis)
        self.chart.removeAxis(self.xAxis)

        if is_log:
            self.xAxis = QLogValueAxis()
            self.xAxis.setBase(10)
        else:
            self.xAxis = QValueAxis()
        self.xAxis.setLabelFormat("%.2e")
        
        self.chart.addAxis(self.xAxis, Qt.AlignBottom)
        for series in self.series.values():
            series.attachAxis(self.xAxis)
        
        self.updateXRange()


    def setLogYAxis(self, is_log=True):
        self.is_y_log = is_log
        logging.debug(f'Setting y axis to {"log" if is_log else "linear"}')

        for series in self.series.values():
            series.detachAxis(self.yAxis)
        self.chart.removeAxis(self.yAxis)

        if is_log:
            self.yAxis = QLogValueAxis()
            self.yAxis.setBase(10)
        else:
            self.yAxis = QValueAxis()
        self.yAxis.setLabelFormat("%.2e")

        self.chart.addAxis(self.yAxis, Qt.AlignLeft)
        for series in self.series.values():
            series.attachAxis(self.yAxis)

        self.updateYRange()


class ModifiedChartView(QChartView):
    mouseMoved = Signal(float, float)
    viewChanged = Signal()

    def __init__(self, chart):
        super(ModifiedChartView, self).__init__(chart)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        super(ModifiedChartView, self).mouseMoveEvent(event)
        widgetPos = event.localPos()
        scenePos = self.mapToScene(widgetPos.x(), widgetPos.y())
        chartPos = self.chart().mapFromScene(scenePos)
        value = self.chart().mapToValue(chartPos)

        self.mouseMoved.emit(value.x(), value.y())

    def mouseReleaseEvent(self, event):
        super(ModifiedChartView, self).mouseReleaseEvent(event)
        self.viewChanged.emit()
