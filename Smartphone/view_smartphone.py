from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from controller_smartphone import *
import sys
import threading
sys.path.append('../')

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Smartphone'
        self.top = 1000
        self.left = 1000
        self.width = 1000
        self.height = 1000
        self.InitWindow()
        self.button = False
        self.start_thread = False

    def button_pressed_start(self):
        thread_status = threading.Thread(target=self.show_message, args=())
        thread_status.start()
        self.button = True
        self.start_thread = True
        start()
        self.connection.setText('<strong>Open connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 14))
        self.connection.adjustSize()
        self.connection.move(60, 350)
    
    def button_pressed_stop(self):
        self.button = False
        self.start_thread = False
        stop()
        self.connection.setText('<strong>Closed connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 14))
        self.connection.adjustSize()
        self.connection.move(60, 350)

    def show_message(self):
        while True:
            if self.start_thread: 
                data = smartphone.get_data_baby_monitor()
                self.send_breathing.setText('Breathing: {}'.format(data['breathing']))
                self.send_breathing.setFont(QtGui.QFont('Arial', 12)) 
                self.send_breathing.adjustSize()
                self.send_breathing.move(60, 130)

                self.send_time_no_breathing.setText('Time no Breathing: {}'.format(data['time_no_breathing']))
                self.send_time_no_breathing.setFont(QtGui.QFont('Arial', 12)) 
                self.send_time_no_breathing.adjustSize() 
                self.send_time_no_breathing.move(60, 150)

                self.send_crying.setText('Crying: {}'.format(data['crying']))
                self.send_crying.setFont(QtGui.QFont('Arial', 12)) 
                self.send_crying.adjustSize() 
                self.send_crying.move(60, 170)

                self.send_sleeping.setText('Sleeping: {}'.format(data['sleeping']))
                self.send_sleeping.setFont(QtGui.QFont('Arial', 12)) 
                self.send_sleeping.adjustSize() 
                self.send_sleeping.move(60, 190)

                if data['time_no_breathing'] > 3:
                    self.alert.setText("Alert: ALERT! Emma isn't breathing")
                    self.alert.setFont(QtGui.QFont('Arial', 12))
                    self.alert.adjustSize()
                    self.alert.move(60, 260)
                else:
                    self.alert.setText("")
                    self.alert.setFont(QtGui.QFont('Arial', 12))
                    self.alert.adjustSize()
                    self.alert.move(60, 260)

    def InitWindow(self):
        # Define image
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('smartphone.png'))
        self.label.setGeometry(400, 50, 512, 512)

        # Define title device
        self.titleDevice = QLabel(self)
        self.titleDevice.setText('<strong>Smartphone<\strong>')
        self.titleDevice.setFont(QtGui.QFont('Arial', 16))
        self.titleDevice.adjustSize()
        self.titleDevice.move(60, 50)

        self.send = QLabel(self)
        self.send.setText('<strong>Receive<\strong>')
        self.send.setFont(QtGui.QFont('Arial', 14))
        self.send.adjustSize()
        self.send.move(60, 100)

        self.connection = QLabel(self)
        self.send_breathing = QLabel(self)
        self.send_time_no_breathing = QLabel(self)
        self.send_crying = QLabel(self)
        self.send_sleeping = QLabel(self)
        self.alert = QLabel(self)

        self.send = QLabel(self)
        self.send.setText('<strong>Send<\strong>')
        self.send.setFont(QtGui.QFont('Arial', 14))
        self.send.adjustSize()
        self.send.move(60, 230)

        self.setWindowIcon(QtGui.QIcon('smartphone.png'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.button = QPushButton('Start', self)
        self.button.move(500, 600)
        self.button.clicked.connect(self.button_pressed_start)

        self.button = QPushButton('Stop', self)
        self.button.move(620, 600)
        self.button.clicked.connect(self.button_pressed_stop)

        self.button = QPushButton('Confirm', self)
        self.button.move(740, 600)
        self.button.clicked.connect(self.button_pressed_stop)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
