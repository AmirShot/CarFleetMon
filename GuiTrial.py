import sys

"""import Mod_PX
from PandasModel import PandasModel"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QTabWidget, QVBoxLayout, QWidget, QMainWindow, QGroupBox, QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
import sqlite3
from DataManager import DataManager

class ProgramWindow(QMainWindow):
    def __init__(self, datamanager: DataManager):
        QMainWindow.__init__(self)
        self.homeDir = "."
        self.setup_main_window()
        self.set_window_layout()
        self.rowCounterTableStats = 0
        self.clicked = False
        self.dataManager = datamanager


    def setup_main_window(self):
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize( 800, 350  )
        self.setWindowTitle( "ProjectX" )

    def set_window_layout(self):
        # buttons
        self.btn_Analisi = QtWidgets.QPushButton('Analisi')
        self.btn_Help = QtWidgets.QPushButton('Help')
        self.btn_Wiz = QtWidgets.QPushButton('Wizard')

        # Initialize tabs_1 screen
        self.tabs_1 = QtWidgets.QTabWidget()
        self.tab1_1 = QtWidgets.QWidget()
        self.tab2_1 = QtWidgets.QWidget()
        self.tab3_1 = QtWidgets.QWidget()
        # Add tabs
        self.tabs_1.addTab(self.tab1_1, "WWA")
        self.tabs_1.addTab(self.tab2_1, "WTP")
        self.tabs_1.addTab(self.tab3_1, "WTW")

        self.btn_Help.clicked.connect(self.showLiveData)

        #initialize table
        colms = ["Licence Plate",
                 "Last Update Date",
                 "Trip Counter",
                 "Update Counter",
                 "Max Speed",
                 "Avg Speed",
                 "Max RPM",
                 "Avg RPM",
                 "Avg Fuel Economy",
                 "Curr Fuel Economy",
                 "Is Online"]
        self.table1 = self.CreateTable(colms, False)


        # Initialize tabs_2 screen
        self.tabs_2 = QtWidgets.QTabWidget()

        self.tab2_2 = QtWidgets.QWidget()
        self.tabs_2.setTabPosition(QtWidgets.QTabWidget.West)
        # Add tabs
        self.tabs_2.addTab(self.table1, "Stats")
        self.tabs_2.addTab(self.tab2_2, "Foglio 2")

        #add Columns
        self.initialTableStatsWithStats()


        self.table_View_1 = QtWidgets.QTableView()
        font = QtGui.QFont()
        font.setPointSize(10)


        # connections
        self.btn_Analisi.clicked.connect(self.loadFile)

        # layouts
        vbox = QtWidgets.QVBoxLayout(self.centralwidget)
        hgroup = QtWidgets.QGroupBox()
        vbox.addWidget(hgroup)
        hlay_group = QtWidgets.QHBoxLayout(hgroup)
        hlay_group.addWidget(self.btn_Analisi)
        hlay_group.addWidget(self.btn_Help)
        hlay_group.addWidget(self.btn_Wiz)
        vbox.addWidget(self.tabs_1)

        lay = QtWidgets.QVBoxLayout(self.tab1_1)
        lay.addWidget(self.tabs_2)

        self.table1.cellClicked.connect(self.showLiveData)

        self.show()


    @pyqtSlot()
    def loadFile(self):
        pass

    def CreateTable(self, values : list, editable: bool):
        table1 = QtWidgets.QTableWidget()
        table1.setColumnCount(len(values))
        table1.setRowCount(2)
        self.rowCounterTableStats = 1
        if not editable:
            table1.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        counter = 0
        for each in values:
            table1.setItem(0, counter, QTableWidgetItem(each))
            counter+=1
        return table1

    def AddValues(self, values : list, table: QTableWidget):
        lst = []
        for each in range(self.rowCounterTableStats-1):
            print(f"row = {each}, col = 0")
            print(f"------------{self.table1.item((each), 0).text()}")
            lst.append(self.table1.item(each,0).text())
        print(lst)
        if values[0] not in lst:
            counter = 0
            for each in values:
                table.setItem(self.rowCounterTableStats-1,counter,QTableWidgetItem(str(each)))
                counter+=1


    def initialTableStatsWithStats(self):
        lst = self.getListOfLists()
        for each in lst:
            print(each)
            self.IncRowCounter()
            self.AddValues(each, self.table1)


    def IncRowCounter(self):
        self.rowCounterTableStats+=1
        self.table1.setRowCount(self.rowCounterTableStats)

    def get_cursor(self):
        print(f'{self.homeDir}/CFM.db')
        sqliteConnection = sqlite3.connect(f'{self.homeDir}/CFM.db')
        return sqliteConnection, sqliteConnection.cursor()

    def getListOfLists(self):
        sql, cursor = self.get_cursor()
        command = f'SELECT * FROM "Stats";'
        cursor.execute(command)
        ret = cursor.fetchall()
        return list(ret)

    def showLiveData(self, licencePlate):
        d1 = dialog(self.table1, licencePlate)

class dialog:
    def __init__(self,table1:QTableWidget, LicencePlate):
        self.d1 = QtWidgets.QDialog()
        self.b1 = QtWidgets.QPushButton("Hello World", self.d1)
        self.b1.move(500, 250)
        self.d1.setGeometry(100, 100, 750, 500)
        self.d1.setWindowTitle("Dialog!")
        self.lbl1 = QtWidgets.QLabel("Nothing", self.d1)
        self.current_row = table1.currentRow()
        self.lbl1.setText(table1.item(self.current_row, 0).text())

        dif = 50
        start = 80
        xPos = 70
        start2 = start - 20
        xPos2 = 600

        self.lblLine = QtWidgets.QLabel("-------------------------------------------------------------", self.d1)
        self.lblLine.setFont(QFont("Ariel", 20))
        self.lblLine.move(xPos, start)

        self.lblLine1 = QtWidgets.QLabel("-------------------------------------------------------------", self.d1)
        self.lblLine1.setFont(QFont("Ariel", 20))
        self.lblLine1.move(xPos, start + dif * 1)

        self.lblLine2 = QtWidgets.QLabel("-------------------------------------------------------------", self.d1)
        self.lblLine2.setFont(QFont("Ariel", 20))
        self.lblLine2.move(xPos, start + dif * 2)

        self.lblLine3 = QtWidgets.QLabel("-------------------------------------------------------------", self.d1)
        self.lblLine3.setFont(QFont("Ariel", 20))
        self.lblLine3.move(xPos, start + dif * 3)

        self.lblLine4 = QtWidgets.QLabel("-------------------------------------------------------------", self.d1)
        self.lblLine4.setFont(QFont("Ariel", 20))
        self.lblLine4.move(xPos, start + dif * 4)

        self.lblLine5 = QtWidgets.QLabel("-------------------------------------------------------------", self.d1)
        self.lblLine5.setFont(QFont("Ariel", 20))
        self.lblLine5.move(xPos, start + dif * 5)

        self.lblLine6 = QtWidgets.QLabel("-------------------------------------------------------------", self.d1)
        self.lblLine6.setFont(QFont("Ariel", 20))
        self.lblLine6.move(xPos, start + dif * 6)

        self.lblLine = QtWidgets.QLabel("Avg Fuel Consumption", self.d1)
        self.lblLine.setFont(QFont("Ariel", 20))
        self.lblLine.move(xPos, start2)

        self.lblText1 = QtWidgets.QLabel("Fuel Consumption", self.d1)
        self.lblText1.setFont(QFont("Ariel", 20))
        self.lblText1.move(xPos, start2 + dif * 1)

        self.lblText2 = QtWidgets.QLabel("Max Speed", self.d1)
        self.lblText2.setFont(QFont("Ariel", 20))
        self.lblText2.move(xPos, start2 + dif * 2)

        self.lblText3 = QtWidgets.QLabel("Current Speed", self.d1)
        self.lblText3.setFont(QFont("Ariel", 20))
        self.lblText3.move(xPos, start2 + dif * 3)

        self.lblText4 = QtWidgets.QLabel("Avg Speed", self.d1)
        self.lblText4.setFont(QFont("Ariel", 20))
        self.lblText4.move(xPos, start2 + dif * 4)

        self.lblText5 = QtWidgets.QLabel("Max RPM", self.d1)
        self.lblText5.setFont(QFont("Ariel", 20))
        self.lblText5.move(xPos, start2 + dif * 5)

        self.lblText6 = QtWidgets.QLabel("Current RPM", self.d1)
        self.lblText6.setFont(QFont("Ariel", 20))
        self.lblText6.move(xPos, start2 + dif * 6)

        self.lblText7 = QtWidgets.QLabel("Avg RPM", self.d1)
        self.lblText7.setFont(QFont("Ariel", 20))
        self.lblText7.move(xPos, start2 + dif * 7)

        self.lblLine10 = QtWidgets.QLabel("KM/L", self.d1)
        self.lblLine10.setFont(QFont("Ariel", 20))
        self.lblLine10.move(xPos2, start2)

        self.lblText11 = QtWidgets.QLabel("KM/L", self.d1)
        self.lblText11.setFont(QFont("Ariel", 20))
        self.lblText11.move(xPos2, start2 + dif * 1)

        self.lblText12 = QtWidgets.QLabel("KMH", self.d1)
        self.lblText12.setFont(QFont("Ariel", 20))
        self.lblText12.move(xPos2, start2 + dif * 2)

        self.lblText13 = QtWidgets.QLabel("KMH", self.d1)
        self.lblText13.setFont(QFont("Ariel", 20))
        self.lblText13.move(xPos2, start2 + dif * 3)

        self.lblText14 = QtWidgets.QLabel("KMH", self.d1)
        self.lblText14.setFont(QFont("Ariel", 20))
        self.lblText14.move(xPos2, start2 + dif * 4)

        self.lblText15 = QtWidgets.QLabel("RPM", self.d1)
        self.lblText15.setFont(QFont("Ariel", 20))
        self.lblText15.move(xPos2, start2 + dif * 5)

        self.lblText16 = QtWidgets.QLabel("RPM", self.d1)
        self.lblText16.setFont(QFont("Ariel", 20))
        self.lblText16.move(xPos2, start2 + dif * 6)

        self.lblText17 = QtWidgets.QLabel("RPM", self.d1)
        self.lblText17.setFont(QFont("Ariel", 20))
        self.lblText17.move(xPos2, start2 + dif * 7)

        self.d1.exec_()


class GUI:
    def __init__(self,datamanager):
        app = QApplication(sys.argv)
        programWindow = ProgramWindow(datamanager)

        programWindow.show()
        sys.exit(app.exec_())