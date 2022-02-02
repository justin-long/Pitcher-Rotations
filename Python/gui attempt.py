# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 16:13:45 2018

@author: jblon
"""

from PyQt5 import QtWidgets
from test_ui import Ui_SIERA

class SieraWindow(QtWidgets.QMainWindow, UiSIERA):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()