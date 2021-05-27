from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

rui = uic.loadUiType("ui/Recharge.ui")[0]

class Recharge_UI(QMainWindow, rui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cp = 0
        # Only int to linedeit
        self.onlyInt = QIntValidator()
        self.APRecharge.setValidator(self.onlyInt)
        # initialization
        self.cur_point()

        # Button/QlineEdit Actions
        self.APRecharge.textChanged.connect(self.aft_point)
        self.Recharge_Btn.clicked.connect(self.recharge_)

        

    # Current Point
    def cur_point(self):
        # get data from the gRPC server

        self.CPoint.setText(str(self.cp))

    # Point After Recharging
    def aft_point(self):
        if self.APRecharge.text() is '':
            par = self.cp
        else:
            par = self.cp + int(float(self.APRecharge.text()))
        self.PointAR.setText(str(par))

    # Recharge Btn
    def recharge_(self):
        # Send the Request to the gRPC server
        
        # After Recharging is done successfully
        self.cp = self.cp + int(float(self.APRecharge.text()))
        self.APRecharge.setText('')
        self.cur_point()