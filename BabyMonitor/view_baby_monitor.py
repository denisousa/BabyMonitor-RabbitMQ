from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Baby Monitor"
        self.top = 1000
        self.left = 1000
        self.width = 1000
        self.height = 1000

        self.InitWindow()

    def InitWindow(self):
        # Define image
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("babymonitor.png"))
        self.label.setGeometry(400, 50, 512, 512)

        # Define title device
        self.titleDevice = QLabel(self)
        self.titleDevice.setText('<strong>Baby Monitor<\strong>')
        self.titleDevice.move(60, 50)

        self.receive = QLabel(self)
        self.receive.setText('<strong>Receive<\strong>')
        self.receive.move(60, 150)

        self.send = QLabel(self)
        self.send.setText('<strong>Send<\strong>')
        self.send.move(60, 250)

        self.setWindowIcon(QtGui.QIcon("babymonitor.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
