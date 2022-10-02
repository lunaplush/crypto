import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, qApp, QMessageBox, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt, QCoreApplication

from PyQt5 import uic
import sys
import os


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
        a = []
        self.btnClose.clicked.connect(QCoreApplication.instance().quit)
        self.chekPandasWork()

    def chekPandasWork(self):
        data = {'Пол': ['мужской', 'женский', 'женский', 'мужской', 'мужской'],
                'Имя': ['Сяо Мин', 'Сяо Хун', 'Сяо Фан', 'Сяо Цян', 'Сяо Мэй'],
                "Возраст": [20, 21, 25, 24, 29]
                }

        df = pd.DataFrame(data, index=['No.1', 'No.2', 'No.3', 'No.4', 'No.5'],
                          columns=['Имя', 'Пол', 'Возраст', 'Род занятий'])
        model = PdTable(df)
        view = self.tableView
        view.setModel(model)
        view.setWindowTitle('Pandas')
        view.setAlternatingRowColors(True)
        view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = mainApp()
    window.chekPandasWork()
    window.show()
    app.exec_()