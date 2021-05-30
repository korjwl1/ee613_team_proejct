from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from .TimerMessage import *
import grpc_code.client_grpc as gp
import data_class as dc

lui = uic.loadUiType("ui/Login.ui")[0]

class LoginUI(QMainWindow, lui):
    def __init__(self, stub):
        super().__init__()
        self.setupUi(self)

        # Button Features
        # singup
        self.SignUp_Btn.clicked.connect(lambda: self.signup(stub))
    
    def login(self, w, stub, MainUI):
        ID = self.Input_ID.text()
        PWD = self.Input_PWD.text()
        # send the User Information to the server and if succec, save it until logout
        success_ = gp.grpc_Login(stub, ID, PWD)

        print(success_)
        
        if success_ is False:
            messagebox = TimerMessageBox(2, self, 'Login Failed')
            messagebox.exec_()
        # show up a popup window for a while and then move on the next ui
        else:
            dc.login_info['id'] = ID
            dc.login_info['pwd'] = PWD
            messagebox = TimerMessageBox(2, self, 'Login Success')
            messagebox.exec_()
            MainUI.get_points(stub, ID, PWD)
            w.setCurrentIndex(1)


    def signup(self, stub):
        ID = self.Input_ID.text()
        PWD = self.Input_PWD.text()

        if gp.grpc_Signup(stub,ID, PWD) is True:
            messagebox = TimerMessageBox(2, self, 'SignUp Success')
            messagebox.exec_()
        else:
            messagebox = TimerMessageBox(2, self, 'SignUp Failed')
            messagebox.exec_()
        # show up a popup window for a while and then close it