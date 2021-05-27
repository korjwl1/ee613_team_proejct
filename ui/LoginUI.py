from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from .TimerMessage import *
import grpc_code.client_grpc as gp

lui = uic.loadUiType("ui/Login.ui")[0]

class LoginUI(QMainWindow, lui):
    def __init__(self, stub):
        super().__init__()
        self.setupUi(self)

        # ID and PWD Save
        self.ID = ''
        self.PWD = ''

        # Button Features
        # singup
        self.SignUp_Btn.clicked.connect(lambda: self.signup(stub))
    
    def login(self, w, stub):
        # send the User Information to the server and if succec, save it until logout

        self.ID = self.Input_ID.text()
        self.PWD = self.Input_PWD.text()
        '''
        menu_info = gp.grpc_Login(stub, self.ID, self.PWD)
        
        if menu_info is None:
            messagebox = TimerMessageBox(2, self, 'Login Failed')
            messagebox.exec_()
        # show up a popup window for a while and then move on the next ui
        else: 
            messagebox = TimerMessageBox(2, self, 'Login Success')
            messagebox.exec_()
            w.setCurrentIndex(1)
        '''
        messagebox = TimerMessageBox(2, self, 'Login Success')
        messagebox.exec_()
        w.setCurrentIndex(1)

    def signup(self, stub):
        self.ID = self.Input_ID.text()
        self.PWD = self.Input_PWD.text()

        if gp.grpc_Signup(stub,self.ID, self.PWD) is True:
            messagebox = TimerMessageBox(2, self, 'SignUp Success')
            messagebox.exec_()
        else:
            messagebox = TimerMessageBox(2, self, 'SignUp Failed')
            messagebox.exec_()
        # show up a popup window for a while and then close it