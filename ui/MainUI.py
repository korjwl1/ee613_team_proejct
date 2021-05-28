from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import grpc_code.client_grpc as gp
import data_class as dc

maui = uic.loadUiType("ui/Main_UI.ui")[0]

class Main_UI(QMainWindow, maui):
    def __init__(self, w):
        super().__init__()
        self.setupUi(self)
        # Button Actions
        self.Order_Btn.clicked.connect(lambda: self.Order_(w))
    
    def get_points(self, stub, usrid, usrpwd):
        # get informations from the gRPC server
        rpoint = gp.grpc_CheckPoint(stub, usrid, usrpwd)
        temp = 'Remaining Points: ' + str(rpoint)
        self.RPoint.setText(temp)
        
    # When the page is loaded
    def initialization(self):
        return None

    def Order_(self, w):
        return None

    def Recharge_(self,stub,w,r_ui):
        r_ui.cur_point(stub,dc.login_info['id'],dc.login_info['pwd'])
        w.setCurrentIndex(3)
        return None