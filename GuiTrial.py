import sys

"""import Mod_PX
from PandasModel import PandasModel"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QTabWidget, QVBoxLayout, QWidget, QMainWindow, QGroupBox, QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSlot
import sqlite3

class ProgramWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.homeDir = "."
        self.setup_main_window()
        self.set_window_layout()
        self.rowCounterTableStats = 0



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
        d1 = QtWidgets.QDialog()
        b1 = QtWidgets.QPushButton("Hello World", d1)
        b1.move(500,250)
        d1.setGeometry(100, 100, 750, 500)
        d1.setWindowTitle("Dialog!")
        lbl1 = QtWidgets.QLabel("Nothing", d1)
        current_row = self.table1.currentRow()
        lbl1.setText(self.table1.item(current_row, 0).text())
        painter = QPainter()
        painter.begin(d1)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.white)
        painter.drawLine(0, 0, 200, 200)




        d1.exec_()

def main():
    app = QApplication(sys.argv)
    programWindow = ProgramWindow()

    programWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()