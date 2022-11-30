import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, qApp, QMessageBox, QTableView, QVBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt, QCoreApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import uic, QtCore
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.dates as mdates

import crypto_data_lib
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
        self.adjust_window()
        self.adjust_functional()
        self.createMenus()
        self.period = crypto_data_lib.Period()
        self.set_period_list()

    def adjust_window(self):
        self.setWindowTitle("Аналитик")
        self.figure = plt.figure(figsize=(30, 20), facecolor="#FFFFFF")
        # self.figure.tight_layout()
        self.canvas = FigureCanvas(self.figure)
        # self.figure.tight_layout()
        self.graph.addWidget(self.canvas)
        self.ax = self.figure.subplots(1, 1)
        self.canvas.figure.set_constrained_layout("constrained")
        cid = self.canvas.mpl_connect('button_press_event', self.onclick_canvas)
        cid2 = self.canvas.mpl_connect('button_release_event', self.onnonclick_canvas)

    # self.viewData("data/BTCUSDT_1d_1502928000000-1589241600000_86400000_1000.csv")

    def adjust_functional(self):
        self.actionOpenFile.triggered.connect(self.onOpenFile)
        self.actionOpenYahoo.triggered.connect(self.onOpenYahoo)
        self.btnClose.clicked.connect(QCoreApplication.instance().quit)
        self.btnRefresh.clicked.connect(self.changePeriod)
        self.btnFullPeriod.clicked.connect(self.returnFullPeriod)
        self.btnLinReg.clicked.connect(self.doLinearRegression)
        self.btnArima.clicked.connect(self.doArima)

    def set_period_list(self):
        slm = QtCore.QStringListModel()
        slm.insertRows(0, 4)
        slm.setData(slm.index(0), "2022/08/20 2022/10/01")
        slm.setData(slm.index(1), "2022/06/22 2022/10/08")
        slm.setData(slm.index(2), "2021/11/11 2022/10/15")
        self.lstPeriod.setModel(slm)
        self.lstPeriod.clicked.connect(self.set_period_from_items)

    def set_period_from_items(self):
        elem = self.lstPeriod.currentIndex()
        (b, e) = elem.data().split()
        self.period.change_begin_period(b, type="str")
        self.period.change_end_period(e, type="str")

        self.txtBeginPeriod.setText(self.period.get_data_format_begin())
        self.txtEndPeriod.setText(self.period.get_data_fromat_end())
        self.btnLinReg.setDisabled(False)
        self.btnArima.setDisabled(False)
        self.btnRefresh.click()

    def onclick_canvas(self, event):
        self.clickPos = event.xdata
        if event.xdata is None:
            print('%s click: button=%d, x=%d, y=%d, outside canvas' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y))
        else:
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))

    def onnonclick_canvas(self, event):
        if event.xdata is None:
            print('%s non click: button=%d, x=%d, y=%d, outside canvas' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y))
        else:
            print('%s non click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
        bPos = self.clickPos
        ePos = event.xdata
        if bPos is None:
            if ePos is None:
                return
            bPos = ePos
        elif ePos is None:
            ePos = bPos
        elif bPos > ePos:
            bPos, ePos = ePos, bPos
        self.period.change_begin_period(bPos)
        self.period.change_end_period(ePos)
        self.txtEndPeriod.setText(self.period.get_data_fromat_end())
        self.txtBeginPeriod.setText(self.period.get_data_format_begin())
        self.btnLinReg.setDisabled(False)
        self.btnArima.setDisabled(False)
        self.btnRefresh.click()

    def createMenus(self):
        menubar = self.menuBar()

    def onOpenFile(self):
        file = QFileDialog.getOpenFileName()
        if file:
           self.df = crypto_data_lib.open_data(file[0])
         #  self.df["date"] = self.df.index
           self.viewData()

    def onOpenYahoo(self):
        try:
            self.df = crypto_data_lib.get_yahoo()
            self.df["price"] = self.df.Low
            self.viewData()
            self.btnLinReg.setDisabled(False)
            self.btnArima.setDisabled(False)
        except OSError:
            pass

    def viewData(self ):

        #cid = self.canvas.mpl_connect('button_press_event', onclick_canvas)

        if hasattr(self, "df"):
            model = PdTable(self.df)
            view = self.tableView
            view.setModel(model)
            view.setWindowTitle('Pandas')
            view.setAlternatingRowColors(True)
            view.show()

            crypto_data_lib.draw_data(self.df, self.ax)

            self.txtBeginPeriod
            #self.graphicsView.setModel(model)
        self.period.change_begin_period(mdates.date2num(self.df.index[0]))
        self.period.change_end_period(mdates.date2num(self.df.index[-1]))
        self.txtBeginPeriod.setText(self.period.get_data_format_begin())
        self.txtEndPeriod.setText(self.period.get_data_fromat_end())

    def changePeriod(self):
        if hasattr(self, "df"):
            crypto_data_lib.draw_data(self.df[self.period.begin:self.period.end], self.ax)

    def returnFullPeriod(self):
        if hasattr(self, "df"):
            crypto_data_lib.draw_data(self.df, self.ax)
            self.period.change_begin_period(mdates.date2num(self.df.index[0]))
            self.period.change_end_period(mdates.date2num(self.df.index[-1]))
            self.txtBeginPeriod.setText(self.period.get_data_format_begin())
            self.txtEndPeriod.setText(self.period.get_data_fromat_end())

    def doLinearRegression(self):
        resVisual = QVBoxLayout()
        self.frame.setLayout(resVisual)
        self.figure2 = plt.figure(figsize=(20, 20), facecolor="#FFFFFF")
        self.canvas2 = FigureCanvas(self.figure2)
        resVisual.addWidget(self.canvas2)
        self.ax2 = self.figure2.subplots(1,1)
        ts = lib2.TimeSeriesPrediction(self.df[self.period.begin:self.period.end])
        ts.plot_linear_regression(ts, self.ax)
        ts.plot_linear_regression(ts, self.ax2)
        self.ax.figure.canvas.draw()
        self.ax2.figure.canvas.draw()

        self.frame.show()

    def doArima(self):
        resVisual = QVBoxLayout()
        self.frame.setLayout(resVisual)
        self.figure2 = plt.figure(figsize=(20, 20), facecolor="#FFFFFF")
        self.canvas2 = FigureCanvas(self.figure2)
        resVisual.addWidget(self.canvas2)
        self.ax2 = self.figure2.subplots(1, 1)
        ts = lib2.TimeSeriesPrediction(self.df[self.period.begin:self.period.end])
        #ts.plot_arima(ts, self.ax)
        ts.plot_arima(ts, self.ax2)
        self.ax.figure.canvas.draw()
        self.ax2.figure.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainApp()
    #window.viewData()
    window.show()
    app.exec_()