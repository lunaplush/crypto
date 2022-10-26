import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, qApp, QMessageBox, QTableView, QVBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt, QCoreApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import uic
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.dates as mdates

import lib1
import lib2


class PdTable(QAbstractTableModel):
    def __init__(self, data):
        super(QAbstractTableModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

        # Данные дисплея

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

        # Отображение заголовка строки и столбца

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.axes[0][col]
        return None





class mainApp(QMainWindow):

    def __init__(self):
        super(mainApp, self).__init__()
        uic.loadUi("base.ui", self)
        self.createMenus()
        self.btnClose.clicked.connect(QCoreApplication.instance().quit)
        self.figure = plt.figure(figsize=(30, 20), facecolor="#FFFFFF")
        #self.figure.tight_layout()
        self.canvas = FigureCanvas(self.figure)
        self.figure.tight_layout()
        self.graph.addWidget(self.canvas)
        self.ax = self.figure.subplots(1, 1)
       # self.viewData("data/BTCUSDT_1d_1502928000000-1589241600000_86400000_1000.csv")
        self.actionOpenFile.triggered.connect(self.onOpenFile)
        cid = self.canvas.mpl_connect('button_press_event', self.onclick_canvas)
        cid2 = self.canvas.mpl_connect('button_release_event', self.onnonclick_canvas)
      # self.df = None
        self.period = lib1.prognoz_period()
        self.btnRefresh.clicked.connect(self.changePeriod)
        self.btnFullPeriod.clicked.connect(self.returnFullPeriod)
        self.btnLinReg.clicked.connect(self.doLinearRegression)



    def onclick_canvas(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        self.period.change_begin_period(event.xdata)

    def onnonclick_canvas(self, event):
        print('%s non click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        self.period.change_end_period(event.xdata)
        self.textBegin.setText(self.period.get_data_format_begin())
        self.textEndTime.setText(self.period.get_data_fromat_end())
        self.btnLinReg.setDisabled(False)

    def createMenus(self):
        menubar = self.menuBar()

    def onOpenFile(self):
        file = QFileDialog.getOpenFileName()
        if file:
           self.viewData(file[0])

    def viewData(self, file = "data/BTCUSDT_1d_1502928000000-1664668800000_86400000_1873.csv" ):

        #cid = self.canvas.mpl_connect('button_press_event', onclick_canvas)
        self.df = lib1.open_data(file)
        self.df["date"] = self.df.index
        if len(self.df):
            model = PdTable(self.df)
            view = self.tableView
            view.setModel(model)
            view.setWindowTitle('Pandas')
            view.setAlternatingRowColors(True)
            view.show()
            lib1.draw_data(self.df, self.ax)
            self.textBegin
            #self.graphicsView.setModel(model)
        self.period.change_begin_period(mdates.date2num(self.df.index[0]))
        self.period.change_end_period(mdates.date2num(self.df.index[-1]))
        self.textBegin.setText(self.period.get_data_format_begin())
        self.textEndTime.setText(self.period.get_data_fromat_end())

    def changePeriod(self):

        lib1.draw_data(self.df[self.period.begin:self.period.end], self.ax)

    def returnFullPeriod(self):
        lib1.draw_data(self.df, self.ax)
        self.period.change_begin_period(mdates.date2num(self.df.index[0]))
        self.period.change_end_period(mdates.date2num(self.df.index[-1]))
        self.textBegin.setText(self.period.get_data_format_begin())
        self.textEndTime.setText(self.period.get_data_fromat_end())

    def doLinearRegression(self):
        resVisual = QVBoxLayout()
        self.frame.setLayout(resVisual)
        self.figure = plt.figure(figsize=(20, 20), facecolor="#FFFFFF")
        self.canvas = FigureCanvas(self.figure)
        resVisual.addWidget(self.canvas)
        self.ax = self.figure.subplots(1,1)
        ts = lib2.TimeSeriesPrediction(self.df[self.period.begin:self.period.end])
        ts.plot_linear_regression(ts, self.ax)

       # self.ax.figure.canvas.draw()
        self.frame.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = mainApp()
    window.viewData()
    window.show()
    app.exec_()