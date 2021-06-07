from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic.properties import QtGui
import data_class as dc
import grpc_code.client_grpc as gp
from .TimerMessage import *

meui = uic.loadUiType("ui/Menu_UI.ui")[0]


class Menu_UI(QMainWindow, meui):
    def __init__(self,stub, w):
        super().__init__()
        self.setupUi(self)
        self.menu_row_list = {}
        self.menu_price = {}
        self.total = 0
        self.Order_Btn.clicked.connect(lambda: self.order(stub))
        self.actionLogOut.triggered.connect(lambda: self.logout(w))
    
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
        return None

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