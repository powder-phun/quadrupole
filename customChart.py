from PySide6.QtWidgets import QWidget, QCheckBox
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QAbstractSeries, QLineSeries
from PySide6.QtCore import Qt, QMargins, Signal, Slot
from PySide6.QtGui import QPainter, QMouseEvent

from ui.time_chart import Ui_timeChart

from parameter import ParameterID, Parameter
from utils import DataPacket, FLOAT_VALIDATOR

TIMESTAMP = "Timestamp"


class CustomChart(QWidget):
    def __init__(self, parent=None):
        super(CustomChart, self).__init__(parent)
        self.chart = QChart()
        self.chartView = ModifiedChartView(self.chart)
        self.ui = None
        self.setupUi()

        self.series: dict[ParameterID, QLineSeries] = {}

        self.xAxis: QValueAxis = QValueAxis()
        self.yAxis: QValueAxis = QValueAxis()

        self.xMin: float = 0
        self.xMax: float = 1
        self.yMin: float = -1
        self.yMax: float = 1

        self.timestamps: list[float] = []

        self.initialize()

        self.checkboxes: dict[ParameterID, QCheckBox] = {}

        self.data: dict[ParameterID, list[float]] = {}
        self.params: dict[ParameterID, Parameter] = None

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
        self.chartView.setRubberBand(self.chartView.RectangleRubberBand)

        # Connecting signals
        self.chartView.mouseMoved.connect(self.mouseMoved)
        self.ui.resetButton.clicked.connect(self.resetView)
        self.chartView.viewChanged.connect(self.viewChanged)


    def setup(self, params: dict[ParameterID, Parameter]):
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

            # Setting lineedits
            self.ui.minXEdit.setValidator(FLOAT_VALIDATOR)
            self.ui.maxXEdit.setValidator(FLOAT_VALIDATOR)
            self.ui.minYEdit.setValidator(FLOAT_VALIDATOR)
            self.ui.maxYEdit.setValidator(FLOAT_VALIDATOR)
            self.ui.minXEdit.returnPressed.connect(self.scaleChanged)
            self.ui.maxXEdit.returnPressed.connect(self.scaleChanged)
            self.ui.minYEdit.returnPressed.connect(self.scaleChanged)
            self.ui.maxYEdit.returnPressed.connect(self.scaleChanged)

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

            # Getting minimal and maximal value
            self.yMin = min(self.yMin, param.minimum)
            self.yMax = max(self.yMax, param.maximum)

    def createSeries(self) -> QAbstractSeries:
        return QLineSeries()

    def addData(self, packet: DataPacket):

        # Saving timestamps
        self.timestamps.append(packet.timestamp)

        # Adding data
        for identifier, value in packet.data.items():
            self.data[identifier].append(value)
        self.updateSeries(packet)

        self.scale()
        
    def checkboxClicked(self, param, value):
        self.series[param].setVisible(value)

        self.yMin = 1e20
        self.yMax = -1e20

        for param, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                self.yMin = min(self.yMin, self.params[param].minimum)
                self.yMax = max(self.yMax, self.params[param].maximum)

        self.yAxis.setRange(self.yMin, self.yMax)

    def clear(self):
        for series in self.series.values():
            series.clear()

    @Slot(float, float)
    def mouseMoved(self, x: float, y: float):
        self.ui.xLabel.setText("{:.2E}".format(x))
        self.ui.yLabel.setText("{:.2E}".format(y))

    def scaleChanged(self):
        self.xMin = float(self.ui.minXEdit.text())
        self.xMax = float(self.ui.maxXEdit.text())
        self.yMin = float(self.ui.minYEdit.text())
        self.yMax = float(self.ui.maxYEdit.text())

        self.xAxis.setRange(self.xMin, self.xMax)
        self.yAxis.setRange(self.yMin, self.yMax)

    def updateXRange(self):
        self.xAxis.setRange(self.xMin, self.xMax)
        self.ui.minXEdit.setText("{:.2E}".format(self.xMin))
        self.ui.maxXEdit.setText("{:.2E}".format(self.xMax))

    def updateYRange(self):
        self.yAxis.setRange(self.yMin, self.yMax)
        self.ui.minYEdit.setText("{:.2E}".format(self.yMin))
        self.ui.maxYEdit.setText("{:.2E}".format(self.yMax))

    def viewChanged(self):
        self.xMin = self.xAxis.min()
        self.xMax = self.xAxis.max()
        self.updateXRange()

        self.yMin = self.yAxis.min()
        self.yMax = self.yAxis.max()
        self.updateYRange()

    def resetView(self):
        self.scale(True)


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
