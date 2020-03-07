from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from model_baby_monitor import get_data_baby_monitor
import sys
sys.path.append('../')
from construct_scenario import bm, engine


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Baby Monitor"
        self.top = 1000
        self.left = 1000
        self.width = 1000
        self.height = 1000
        self.get_data_baby_monitor = get_data_baby_monitor
        self.bm = bm
        self.engine = engine
        self.InitWindow()

    def InitWindow(self):
        data = self.get_data_baby_monitor(self.bm, self.engine)
        # Define image
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("babymonitor.png"))
        self.label.setGeometry(400, 50, 512, 512)

        # Define title device
        self.titleDevice = QLabel(self)
        self.titleDevice.setText('<strong>Smartphone<\strong>')
        self.titleDevice.setFont(QtGui.QFont('Arial', 16))
        self.titleDevice.adjustSize()
        self.titleDevice.move(60, 50)

        '''
        self.receive = QLabel(self)
        self.receive.setText('<strong>Receive<\strong>')
        self.receive.setFont(QtGui.QFont('Arial', 14))
        self.receive.adjustSize()
        self.receive.move(60, 130)

        self.receive_information = QLabel(self)
        self.receive_information.setText('Information')
        self.receive.setFont(QtGui.QFont('Arial', 12))
        self.receive.adjustSize()
        self.receive_information.move(60, 160)
        '''
        self.send = QLabel(self)
        self.send.setText('<strong>Send<\strong>')
        self.send.setFont(QtGui.QFont('Arial', 14))
        self.send.adjustSize()
        self.send.move(60, 100)

        self.send_breathing = QLabel(self)
        self.send_breathing.setText('Breathing: {}'.format(data[1]))
        self.send_breathing.setFont(QtGui.QFont('Arial', 12)) 
        self.send_breathing.adjustSize()
        self.send_breathing.move(60, 130)

        self.send_time_no_breathing = QLabel(self)
        self.send_time_no_breathing.setText('Time no Breathing: {}'.format(data[2]))
        self.send_time_no_breathing.setFont(QtGui.QFont('Arial', 12)) 
        self.send_time_no_breathing.adjustSize() 
        self.send_time_no_breathing.move(60, 150)

        self.send_time_no_breathing = QLabel(self)
        self.send_time_no_breathing.setText('Crying: {}'.format(data[3]))
        self.send_time_no_breathing.setFont(QtGui.QFont('Arial', 12)) 
        self.send_time_no_breathing.adjustSize() 
        self.send_time_no_breathing.move(60, 170)

        self.send_time_no_breathing = QLabel(self)
        self.send_time_no_breathing.setText('Sleeping: {}'.format(data[4]))
        self.send_time_no_breathing.setFont(QtGui.QFont('Arial', 12)) 
        self.send_time_no_breathing.adjustSize() 
        self.send_time_no_breathing.move(60, 190)

        self.setWindowIcon(QtGui.QIcon("babymonitor.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
