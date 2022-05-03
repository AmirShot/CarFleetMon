from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

class Window(QMainWindow):

    def __init__(self):

        super().__init__()

        self.title = "PyQt5 Drawing Tutorial"

        self.top= 150

        self.left= 150

        self.width = 500

        self.height = 500

        self.InitWindow()

    def InitWindow(self):

        self.setWindowTitle(self.title)

        self.setGeometry(self.top, self.left, self.width, self.height)

        self.show()

        painter = QPainter()

        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QtCore.Qt.red)

        painter.setBrush(QtCore.Qt.white)

        painter.drawLine(400, 100, 100, 100)


App = QApplication(sys.argv)

window = Window()

sys.exit(App.exec())