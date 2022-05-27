import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QTabWidget, QVBoxLayout, QWidget, QMainWindow, QGroupBox, QTableWidget,QTableWidgetItem,QMdiSubWindow, QDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
import sqlite3
from DataManager import DataManager
from ConnectionManager import ConnectionManager
from proto1_pb2 import *
import threading
from proto1_pb2 import *

class login(QDialog):
    def __init__(self):
        #, datamanager: DataManager
        super(login, self).__init__()
        self.setup_main_window()
        self.designUI()

    def setup_main_window(self):
        self.widget = QWidget(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.resize( 1200, 1000)
        self.setWindowTitle( "ProjectX" )

    def designUI(self):
        self.inputUserNameLogin = QtWidgets.QLineEdit()
        self.labelUserName = QtWidgets.QLabel(text="login:")
        self.btnSwitchScreens = QtWidgets.QPushButton(text="switch")
        self.layout.addWidget(self.labelUserName)
        self.layout.addWidget(self.inputUserNameLogin)
        self.layout.addWidget(self.btnSwitchScreens)
        self.labelUserName.move(100, 100)
        self.inputUserNameLogin.move(100, 150)
        self.btnSwitchScreens.clicked.connect(self.switchTo)

    def switchTo(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)

class register(QDialog):
    def __init__(self):
        #, datamanager: DataManager
        super(register, self).__init__()
        self.setup_main_window()
        self.designUI()

    def setup_main_window(self):
        self.widget = QWidget(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.resize( 1200, 1000)
        self.setWindowTitle( "ProjectX" )

    def designUI(self):
        self.inputUserNameLogin = QtWidgets.QLineEdit()
        self.labelUserName = QtWidgets.QLabel(text="Register:")
        self.btnSwitchScreens = QtWidgets.QPushButton(text="switch")
        self.layout.addWidget(self.labelUserName)
        self.layout.addWidget(self.inputUserNameLogin)
        self.layout.addWidget(self.btnSwitchScreens)
        self.labelUserName.move(100,100)
        self.inputUserNameLogin.move(100, 150)
        self.btnSwitchScreens.clicked.connect(self.switchTo)

    def switchTo(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
mainwindow = login()
registerWindow = register()
widget.addWidget(mainwindow.widget)
widget.addWidget(registerWindow.widget)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")



