from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

meui = uic.loadUiType("ui/Menu_UI.ui")[0]


class Menu_UI(QMainWindow, meui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        