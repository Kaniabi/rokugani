# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from .main_window_ui import Ui_MainWindow



class MainWindow(Ui_MainWindow):

    def __init__(self):
        self._window = QtWidgets.QMainWindow()
        self.setupUi(self._window)


    def show(self):
        self._window.show()
