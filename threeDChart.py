from PySide6.QtWidgets import QWidget, QCheckBox
from PySide6.QtCharts import QChartView, QChart, QValueAxis, QAbstractSeries, QLineSeries
from PySide6.QtCore import Qt, QMargins, Signal, Slot
from PySide6.QtGui import QPainter, QMouseEvent

from ui.three_d_chart import Ui_threeDChart

from parameter import ParameterID, Parameter
from utils import DataPacket, FLOAT_VALIDATOR

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

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
        self.fig = None
        self.ax = None

    def setup(self, params: dict[ParameterID, Parameter]):
        self.params = params
        self.setupUi()
        self.setupPlot()

        # Add params to combobox
        for param in self.params.values():
            self.ui.zAxisCombobox.addItem(param.name)

        # Setup empty data matrixes
        for param in self.params.keys():
            self.data[param] = [[0]]

        # Connect combobox event
        self.ui.zAxisCombobox.currentTextChanged.connect(self.comboboxChanged)
        self.comboboxChanged(self.ui.zAxisCombobox.currentText())

    def setupPlot(self):
        data = [[0]]
        self.fig, self.ax = plt.subplots()
        self.imshow = self.ax.imshow(data)
        # plot
        self.plotWidget = FigureCanvas(self.fig)
        self.ui.horizontalLayout.replaceWidget(self.ui.chart, self.plotWidget)

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
            self.data[parameter] = np.zeros((stepX, stepY))

        # Saving sweep parameters to be able to index data based on values
        self.xDataMin = minX
        self.xDataMax = maxX
        self.xDataSteps = stepX
        self.xParam = paramX
        self.yDataMin = minY
        self.yDataMax = maxY
        self.yDataSteps = stepY
        self.yParam = paramY

    def addData(self, packet: DataPacket):
        # Adding data
        x = int((packet.data[self.xParam] - self.xDataMin) / ((self.xDataMax-self.xDataMin)/(self.xDataSteps-1)))
        y = int((packet.data[self.yParam] - self.yDataMin) / ((self.yDataMax-self.yDataMin)/(self.yDataSteps-1)))
        print(x, packet.data[self.xParam], self.xDataMin, self.xDataMax, self.xDataSteps)
        for identifier, value in packet.data.items():
            self.data[identifier][x][y] = value
    
        self.draw()


    def draw(self):
        # self.data[self.selected]
        data = np.random.random((16, 16))

        self.imshow.vmin = np.amin(data)
        self.imshow.vmax = np.amax(data)
        self.imshow.set_data(data)
        # self.fig.canvas.cla()
        self.fig.canvas.draw_idle()
        self.show()
        
    def comboboxChanged(self, text):
        identifier = next(
            param.id for param in self.params.values() if param.name == text
        )
        self.selected = identifier

        self.draw()