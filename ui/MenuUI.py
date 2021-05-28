from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.uic.properties import QtGui

meui = uic.loadUiType("ui/Menu_UI.ui")[0]


class Menu_UI(QMainWindow, meui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.menu_spinbox_list = {}
        self.addMenuWidgets()
        
    # Adding the Menu line to the ui
    def menu_line_add(self):
        return None

    def total_cost(self):
        return None
    
    def voice(self):
        return None

    def createMenuRow(self):
        menu_row = QWidget()
        layout_ = QHBoxLayout()
        layout_.addWidget(QLabel('IMG2' , self))
        layout_.addWidget(QLabel('Menu2', self))
        layout_.addWidget(QLabel('Price2', self))
        layout_.addWidget(QLabel('Quantity2', self))
        layout_.addWidget(QSpinBox(self))
        menu_row.setLayout(layout_)
        self.scrollwidget.layout().addWidget(menu_row)

    def addMenuWidgets(self):
        self.createMenuRow()
        self.scrollwidget.layout().addItem(QSpacerItem(20,40,QSizePolicy.Expanding))