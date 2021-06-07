from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic.properties import QtGui
import data_class as dc
import grpc_code.client_grpc as gp
from .TimerMessage import *


import speech_recognition as sr

meui = uic.loadUiType("ui/Menu_UI.ui")[0]


class Menu_UI(QMainWindow, meui):
    def __init__(self,stub, w):
        super().__init__()
        self.setupUi(self)
        self.menu_row_list = {}
        self.menu_price = {}
        self.total = 0
        self.Order_Btn.clicked.connect(lambda: self.order(stub))
        self.Voice_Btn.clicked.connect(lambda: self.voice())
        self.actionLogOut.triggered.connect(lambda: self.logout(w))
        self.SR = sr.Recognizer()
    
    def logout(self,  w):
        dc.login_info['id'] = ''
        dc.login_info['pwd'] = ''
        w.setCurrentIndex(0)
        
    # Adding the Menu line to the ui
    def order(self,stub):
        # only the menu_id and menu_num, total_cost is needed
        # menu_id: menu_num
        orders_info = {}
        # find the menus without 0 order
        for menu_id in dc.menu_info:
            a = self.menu_row_list[menu_id].children()[5].value()
            if  a !=  0:
                orders_info[menu_id] = a
        success_, rpoint = gp.grpc_OrderFood(stub,orders_info, self.total)
        if success_:
            me_msg = 'Order Success\nRemanining Points: ' + str(rpoint)
        else:
            me_msg = 'Order Failed\nRemanining Points: ' + str(rpoint)
        messagebox = TimerMessageBox(2, self, me_msg)
        messagebox.exec_()
        # for refreshing
        gp.grpc_Login(stub, dc.login_info['id'], dc.login_info['pwd'])
        self.addMenuWidgets()

    def total_cost(self):
        self.total = 0
        for menu_id in dc.menu_info:
            self.total += self.menu_price[menu_id] * self.menu_row_list[menu_id].children()[5].value()
        self.total_c.setText(str(self.total))
    
    def voice(self):
        # dc.menu_info[0][2] = 4
        # mic functions

        text = self.SR.read_from_microphone()
        
        words = self.SR.voice_str_parser(text)
        
        me_msg = "Your order:  " + " ".join(words)
        messagebox = TimerMessageBox(5, self, me_msg)
        messagebox.exec_()

        #process words
        #case   convert numbers to word numbers 
        nums = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}

        # foods dict creation
        foods = {}
        for ids in dc.menu_info:
            foods[dc.menu_info[ids][0]] = ids


        order_data = {} 
        # dictionary {'menu_id' : '# of order'} 
        for i in range(len(words)):
            if words[i] in nums: 
                if words[i+1] in foods:
                    #print(nums[words[i]], foods[words[i+1]])
                    order_data[foods[words[i+1]]] = nums[words[i]]
        print("dictionary = {menuid: order number}")            
        print(order_data)

        
       # olist={0: 1, 4: 1, 3: 1, 6: 1, 2: 1}
        for i in order_data:
            self.menu_row_list[i].children()[5].setValue(order_data[i])

        #return None

    def createMenuRow(self, menu_id, menu_name, menu_price, menu_num):
        menu_row = QWidget()
        layout_ = QHBoxLayout()
        layout_.addWidget(QLabel('IMG' , self))
        layout_.addWidget(QLabel(menu_name, self))
        layout_.addWidget(QLabel(str(menu_price), self))
        layout_.addWidget(QLabel(str(menu_num), self))
        spinbox = QSpinBox(self)
        spinbox.setMaximum(menu_num)
        spinbox.valueChanged.connect(self.total_cost)
        layout_.addWidget(spinbox)
        menu_row.setLayout(layout_)
        self.scrollwidget.layout().addWidget(menu_row)
        self.menu_row_list[menu_id] = menu_row
        self.menu_price[menu_id] = menu_price
        # menu_row.children() - > 0: layout_ 1: IMG 2: menu_name 3: menu_price 4: menu_num 5: spinbox
    
    def editMenuRow(self, menu_id, menu_name, menu_price, menu_num):
        self.menu_row_list[menu_id].children()[2].setText(menu_name)
        self.menu_row_list[menu_id].children()[3].setText(str(menu_price))
        self.menu_row_list[menu_id].children()[4].setText(str(menu_num))
        self.menu_row_list[menu_id].children()[5].setMaximum(menu_num)
        self.menu_price[menu_id] = menu_price

    def addMenuWidgets(self):
        # According to the menu info received from the server, make the menu rows
        for menu_id in dc.menu_info:
            if menu_id not in self.menu_row_list:
                self.createMenuRow(menu_id, dc.menu_info[menu_id][0], dc.menu_info[menu_id][1], dc.menu_info[menu_id][2])
            else:
                self.editMenuRow(menu_id, dc.menu_info[menu_id][0], dc.menu_info[menu_id][1], dc.menu_info[menu_id][2])

        # Vertical Spacer
        if not bool(self.menu_row_list):
            self.scrollwidget.layout().addItem(QSpacerItem(20,40,QSizePolicy.Expanding))