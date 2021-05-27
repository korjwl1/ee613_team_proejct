from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

maui = uic.loadUiType("ui/Main_UI.ui")[0]

class Main_UI(QMainWindow, maui):
    def __init__(self, w):
        super().__init__()
        self.setupUi(self)
        # Point
        self.get_points()
        # Button Actions
        self.Order_Btn.clicked.connect(lambda: self.Order_(w))
        self.Recharge_Btn.clicked.connect(lambda: self.Recharge_(w))
    
    def get_points(self):
        # get informations from the gRPC server

        temp = 'Remaining Points: ' + str(0)
        self.RPoint.setText(temp)
        
    # When the page is loaded
    def initialization(self):
        return None

    def Order_(self, w):
        return None

    def Recharge_(self,w):
        return None