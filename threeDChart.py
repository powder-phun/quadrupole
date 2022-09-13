from PySide6.QtWidgets import QWidget, QCheckBox
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QAbstractSeries, QLineSeries
from PySide6.QtCore import Qt, QMargins, Signal, Slot
from PySide6.QtGui import QPainter, QMouseEvent

from ui.three_d_chart import Ui_threeDChart

from parameter import ParameterID, Parameter
from utils import DataPacket, FLOAT_VALIDATOR

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import Normalize


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class ThreeDChart(QWidget):
    def __init__(self, parent=None):
        super(ThreeDChart, self).__init__(parent)
        self.ui = None

        self.xMin: float = 0
        self.xMax: float = 1
        self.yMin: float = -1
        self.yMax: float = 1
        self.zMin: float = 0
        self.zMax: float = 1

        self.xDataMin: float = 0
        self.xDataMax: float = 1
        self.xDataSteps: int = 1
        self.xParam: ParameterID = None
        self.yDataMin: float = 0
        self.yDataMax: float = 1
        self.yDataSteps: int = 1
        self.yParam: ParameterID = None

        self.data: dict[ParameterID, Any] = {}
        self.params: dict[ParameterID, Parameter] = None

        self.plotWidget = None
        self.imshow = None
        self.selected = None

    def setup(self, params: dict[ParameterID, Parameter]):
        self.params = params
        self.setupUi()
        self.setupPlot()

        # Add params to combobox
        for param in self.params.values():
            self.ui.zAxisCombobox.addItem(param.name)

        # Setup empty data matrixes
        for param in self.params.keys():
            self.data[param] = np.random.random((5, 5))

        # Connect combobox event
        self.ui.zAxisCombobox.currentTextChanged.connect(self.comboboxChanged)
        self.comboboxChanged(self.ui.zAxisCombobox.currentText())

    def setupPlot(self):
        self.plotWidget = MplCanvas(self)
        self.ui.horizontalLayout.replaceWidget(self.ui.chart, self.plotWidget)
        data = np.random.random((5, 5))
        self.imshow = self.plotWidget.axes.imshow(data, origin='lower')

        # show window
        self.show() 

    def setupUi(self):
        self.ui = Ui_threeDChart()
        self.ui.setupUi(self)

    def setRanges(self, paramX: ParameterID, paramY: ParameterID, minX: float, maxX: float, stepX:int, minY: float, maxY: float, stepY: int):
        # Deleting old data
        self.data = {}
        for param in self.params.keys():
            self.data[param] = [[0]]
        
        # Seting up new matrices
        for parameter in self.params.keys():
            self.data[parameter] = np.zeros((stepY, stepX))

        # Saving sweep parameters to be able to index data based on values
        self.xDataMin = minX
        self.xDataMax = maxX
        self.xDataSteps = stepX
        self.xParam = paramX
        self.yDataMin = minY
        self.yDataMax = maxY
        self.yDataSteps = stepY
        self.yParam = paramY

        # Replacing imshow with new one with new dimensions
        newPlotWidget = MplCanvas(self)
        self.ui.horizontalLayout.replaceWidget(self.plotWidget, newPlotWidget)
        self.plotWidget = newPlotWidget
        data = np.random.random((stepY, stepX))
        self.imshow = self.plotWidget.axes.imshow(data, origin='lower')

        self.createLabels()

        self.plotWidget.axes.set_xlabel(self.params[self.xParam].name)
        self.plotWidget.axes.set_ylabel(self.params[self.yParam].name)
        self.plotWidget.fig.tight_layout()

    def addData(self, packet: DataPacket):
        # Adding data
        x = packet.step % self.xDataSteps
        y = int(packet.step / self.xDataSteps)
        for identifier, value in packet.data.items():
            self.data[identifier][y][x] = value

        # Redrawing
        self.draw()


    def draw(self):
        # Normalize data to [0, 1]
        data = self.data[self.selected]
        self.imshow.set_norm(Normalize(np.amin(data), np.amax(data)))
        # Set new data and redraw
        self.imshow.set_data(data)
        self.plotWidget.draw()

    def comboboxChanged(self, text):
        # Read set parameter and save it
        identifier = next(
            param.id for param in self.params.values() if param.name == text
        )
        self.selected = identifier

        # Draw new graph
        self.draw()

    def createLabels(self):
        x_count = min(self.xDataSteps, 6) # Get count of ticks
        x_positions = np.linspace(0, self.xDataSteps-1, num=x_count) # Distribute ticks linearly
        x_values = np.linspace(self.xDataMin, self.xDataMax, num=x_count) # Get label values
        x_labels = [f"{value:.2e}" for value in x_values] # Format labels in scientific notation
        self.plotWidget.axes.set_xticks(x_positions, x_labels) # Set new ticks and labels
        self.plotWidget.axes.tick_params(axis="x", labelrotation=90) # Set label orientation

        # Same for y
        y_count = min(self.yDataSteps, 6) # Get count of ticks
        y_positions = np.linspace(0, self.yDataSteps-1, num=y_count) # Distribute ticks linearly
        y_values = np.linspace(self.yDataMin, self.yDataMax, num=y_count) # Get label values
        y_labels = [f"{value:.2e}" for value in y_values] # Format labels in scientific notation
        self.plotWidget.axes.set_yticks(y_positions, y_labels) # Set new ticks and labels
