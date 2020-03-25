from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from controller_smart_tv import *
import sys
import threading
sys.path.append('../')

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Baby Monitor'
        self.top = 1000
        self.left = 1000
        self.width = 1000
        self.height = 1000
        self.start_thread = False
        self.InitWindow()

    def button_pressed_start(self):
        smart_tv_turn_on()
        thread_status = threading.Thread(target=self.show_message, args=())
        thread_status.start()
        #self.button = True
        self.start_thread = True
        self.connection.setText('<strong>Open connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 14))
        self.connection.adjustSize()
        self.connection.move(60, 350)
    
    def button_pressed_stop(self):
        #self.button = False
        self.start_thread = False
        turn_off()
        self.connection.setText('<strong>Closed connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 14))
        self.connection.adjustSize()
        self.connection.move(60, 350)

    def button_pressed_start_app(self):
        start_app()

    
    def button_pressed_stop_app(self):
        stop_app()


    def show_message(self):
        while True:
            if self.start_thread: 
                if smart_tv.status:
                    self.status.setText('TV is unlocked')
                    self.status.setFont(QtGui.QFont('Arial', 12)) 
                    self.status.adjustSize()
                    self.status.move(60, 130)
                else:
                    self.status.setText('TV is locked')
                    self.status.setFont(QtGui.QFont('Arial', 12)) 
                    self.status.adjustSize()
                    self.status.move(60, 130)

                if smart_tv.application:
                    self.app.setText('App running')
                    self.app.setFont(QtGui.QFont('Arial', 12)) 
                    self.app.adjustSize()
                    self.app.move(60, 160)
                elif not smart_tv.application:
                    self.app.setText('App stop')
                    self.app.setFont(QtGui.QFont('Arial', 12)) 
                    self.app.adjustSize()
                    self.app.move(60, 160)
                elif smart_tv.application == None:
                    self.app.setText('')
                    self.app.setFont(QtGui.QFont('Arial', 12)) 
                    self.app.adjustSize()
                    self.app.move(60, 160)


    def InitWindow(self):

        # Define title device
        self.titleDevice = QLabel(self)
        self.titleDevice.setText('<strong>Smart TV<\strong>')
        self.titleDevice.move(60, 50)

        self.receive = QLabel(self)
        self.receive.setText('<strong>Status<\strong>')
        self.receive.move(60, 100)

        self.receive = QLabel(self)
        self.receive.setText('<strong>Receive<\strong>')
        self.receive.move(60, 230)

        self.receive = QLabel(self)
        self.receive.setText('<strong>Information<\strong>')
        self.receive.move(60, 320)

        self.button_turn_on = QPushButton('Turn On', self)
        self.button_turn_on.move(480, 600)
        self.button_turn_on.clicked.connect(self.button_pressed_start)

        self.button_turn_off = QPushButton('Turn Off', self)
        self.button_turn_off.move(600, 600)
        self.button_turn_off.clicked.connect(self.button_pressed_stop)

        self.button_start_app = QPushButton('Start App', self)
        self.button_start_app.move(720, 600)
        self.button_start_app.clicked.connect(self.button_pressed_start_app)

        self.button_stop_app = QPushButton('Stop App', self)
        self.button_stop_app.move(840, 600)
        self.button_stop_app.clicked.connect(self.button_pressed_stop_app)


        self.status = QLabel(self)
        self.app = QLabel(self)
        self.connection = QLabel(self)

        '''self.send_breathing = QLabel(self)
        self.send_time_no_breathing = QLabel(self)
        self.send_crying = QLabel(self)
        self.send_sleeping = QLabel(self)
        self.message_from_smartphone = QLabel(self)
        self.pending = QLabel(self)'''

        # Define image
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('monitor.svg'))
        self.label.setGeometry(400, 50, 512, 512)

        self.setWindowIcon(QtGui.QIcon('monitor.svg'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
