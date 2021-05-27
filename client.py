from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui.LoginUI import *
from ui.MainUI import *
from ui.MenuUI import *
from ui.ReUI import *
import grpc_code.client_grpc as gp
from SpeechRecognition import *
import sys

from PyQt5.uic.properties import QtWidgets



if __name__ == '__main__':
    # gRPC Initialization
    stub = gp.grpc_Initialize()

    # QT Initialization
    app=QApplication(sys.argv)
    w = QStackedWidget()
    login_ui = LoginUI(stub)
    ma_ui = Main_UI(w)
    me_ui = Menu_UI()
    r_ui = Recharge_UI()
    w.addWidget(login_ui)
    w.addWidget(ma_ui)
    w.addWidget(me_ui)
    w.addWidget(r_ui)

    # UI Transitions
    # login
    login_ui.Login_Btn.clicked.connect(lambda: login_ui.login(w, stub))
    login_ui.Input_ID.returnPressed.connect(lambda: login_ui.login(w, stub))
    login_ui.Input_PWD.returnPressed.connect(lambda: login_ui.login(w, stub))
    # order menu
    ma_ui.Order_Btn.clicked.connect(lambda: w.setCurrentIndex(2))
    # recharge menu
    ma_ui.Recharge_Btn.clicked.connect(lambda: w.setCurrentIndex(3))
    # return
    me_ui.Return_Btn.clicked.connect(lambda: w.setCurrentIndex(1))
    r_ui.Return_Btn.clicked.connect(lambda: w.setCurrentIndex(1))
    # initial window size
    w.resize(440,550)
    w.show()
    app.exec_()