from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import grpc_code.client_grpc as gp
import data_class as dc

rui = uic.loadUiType("ui/Recharge.ui")[0]

class Recharge_UI(QMainWindow, rui):
    def __init__(self, stub, w):
        super().__init__()
        self.setupUi(self)
        self.cp = 0
        # Only int to linedeit
        self.onlyInt = QIntValidator()
        self.APRecharge.setValidator(self.onlyInt)
        # initialization

        # Button/QlineEdit Actions
        self.APRecharge.textChanged.connect(self.aft_point)
        self.Recharge_Btn.clicked.connect(lambda: self.recharge_(stub))
        self.actionLogOut.triggered.connect(lambda: self.logout(w))

    def logout(self,  w):
        dc.login_info['id'] = ''
        dc.login_info['pwd'] = ''
        w.setCurrentIndex(0)

    # Current Point
    def cur_point(self, stub, usrid, usrpwd):
        # get data from the gRPC server
        self.cp = gp.grpc_CheckPoint(stub, usrid, usrpwd)        
        self.CPoint.setText(str(self.cp))

    # Point After Recharging
    def aft_point(self):
        if self.APRecharge.text() == '':
            par = self.cp
        else:
            par = self.cp + int(float(self.APRecharge.text()))
        self.PointAR.setText(str(par))

    # Recharge Btn
    def recharge_(self, stub):
        # Send the Request to the gRPC server
        gp.grpc_RechargePoint(stub, dc.login_info['id'], dc.login_info['pwd'], int(float(self.APRecharge.text())))
        # After Recharging is done successfully
        self.cur_point(stub, dc.login_info['id'], dc.login_info['pwd'])
        self.APRecharge.setText('')
    
    def return_(self,stub,w,ma_ui):
        ma_ui.get_points(stub, dc.login_info['id'], dc.login_info['pwd'])
        w.setCurrentIndex(1)