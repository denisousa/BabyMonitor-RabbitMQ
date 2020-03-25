from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import sys
sys.path.append('./BabyMonitor')
sys.path.append('./Smartphone')
sys.path.append('./SmartTv')
from BabyMonitor.controller_baby_monitor import *
from Smartphone.controller_smartphone import *
from SmartTv.controller_smart_tv import *
import threading
from functools import partial

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Projecy Babymonitor - IoT"
        self.top = 1000
        self.left = 1000
        self.width = 2000
        self.height = 2000
        self.button = False
        self.start_thread = False
        self.InitWindow()

    def button_pressed_start(self, device):
        if device == 'baby_monitor':
            baby_monitor_start()
            self.button = True
            self.start_thread = True
            thread_status = threading.Thread(target=self.baby_monitor_show_message, args=())
            thread_status.start()
        elif device == 'smartphone':
            pass
        else:
            pass
        self.connection.setText('<strong>Open connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 12))
        self.connection.adjustSize()
        self.connection.move(70, 550)
    
    def button_pressed_stop(self, device):
        if device == 'baby_monitor':
            self.button = False
            self.start_thread = False
            baby_monitor_stop()
        elif device == 'smartphone':
            pass
        else:
            pass
        self.connection.setText('<strong>Closed connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 12))
        self.connection.adjustSize()
        self.connection.move(70, 550)

    def baby_monitor_show_message(self):
        global position_x
        while True:
            if self.start_thread: 
                data = baby_monitor_get_data()
                self.send_breathing.setText('Breathing: {}'.format(data['breathing']))
                self.send_breathing.setFont(QtGui.QFont('Arial', 12)) 
                self.send_breathing.adjustSize()
                self.send_breathing.move(70, 230)

                self.send_time_no_breathing.setText('Time no Breathing: {}'.format(data['time_no_breathing']))
                self.send_time_no_breathing.setFont(QtGui.QFont('Arial', 12)) 
                self.send_time_no_breathing.adjustSize() 
                self.send_time_no_breathing.move(70, 250)

                self.send_crying.setText('Crying: {}'.format(data['crying']))
                self.send_crying.setFont(QtGui.QFont('Arial', 12)) 
                self.send_crying.adjustSize() 
                self.send_crying.move(70, 270)

                self.send_sleeping.setText('Sleeping: {}'.format(data['sleeping']))
                self.send_sleeping.setFont(QtGui.QFont('Arial', 12)) 
                self.send_sleeping.adjustSize() 
                self.send_sleeping.move(70, 290)

                if 'Pending' in baby_monitor_get_confirmation():
                    self.pending.setText(baby_monitor_get_confirmation())
                    self.pending.setFont(QtGui.QFont('Arial', 12)) 
                    self.pending.adjustSize() 
                    self.pending.move(70, 460)
                    self.message_from_smartphone.setText("")
                else:
                    self.message_from_smartphone.setText(baby_monitor_get_confirmation())
                    self.message_from_smartphone.setFont(QtGui.QFont('Arial', 12)) 
                    self.message_from_smartphone.adjustSize() 
                    self.message_from_smartphone.move(70, 460)
                    self.pending.setText("")

    def create_interface(self, position_x, name_interface):
        # Define title device
        self.title_baby_monitor = QLabel(self)
        self.title_baby_monitor.setText('<strong>{}<\strong>'.format(name_interface))
        self.title_baby_monitor.setFont(QtGui.QFont('Arial', 16))
        self.title_baby_monitor.adjustSize()
        self.title_baby_monitor.move(position_x, 10)

        self.send = QLabel(self)
        self.send.setText('<strong>Send<\strong>')
        self.send.setFont(QtGui.QFont('Arial', 14))
        self.send.adjustSize()
        self.send.move(position_x, 200)

        self.receive = QLabel(self)
        self.receive.setText('<strong>Receive<\strong>')
        self.receive.setFont(QtGui.QFont('Arial', 14))
        self.receive.adjustSize()
        self.receive.move(position_x, 320)

        self.information = QLabel(self)
        self.information.setText('<strong>Information<\strong>')
        self.information.setFont(QtGui.QFont('Arial', 14))
        self.information.adjustSize()
        self.information.move(position_x, 420)

        self.connection = QLabel(self)
        self.send_breathing = QLabel(self)
        self.send_time_no_breathing = QLabel(self)
        self.send_crying = QLabel(self)
        self.send_sleeping = QLabel(self)
        self.message_from_smartphone = QLabel(self)
        self.pending = QLabel(self)
        
        if name_interface == 'Baby Monitor':
            self.button = QPushButton('Start', self)
            self.button.move(position_x - 20, 600)
            self.button.clicked.connect(partial(self.button_pressed_start, 'baby_monitor'))
            self.button = QPushButton('Stop', self)
            self.button.move(position_x + 100, 600)
            self.button.clicked.connect(partial(self.button_pressed_stop, 'baby_monitor'))
        elif name_interface == 'Smartphone':
            self.button = QPushButton('Start', self)
            self.button.move(position_x - 20, 600)
            self.button.clicked.connect(partial(self.button_pressed_start, 'smartphone'))
            self.button = QPushButton('Stop', self)
            self.button.move(position_x + 100, 600)
            self.button.clicked.connect(partial(self.button_pressed_stop, 'smartphone'))
        else:
            self.button = QPushButton('Start', self)
            self.button.move(position_x - 20, 600)
            self.button.clicked.connect(partial(self.button_pressed_start, 'tv'))
            self.button = QPushButton('Stop', self)
            self.button.move(position_x + 100, 600)
            self.button.clicked.connect(partial(self.button_pressed_stop, 'tv'))



    def InitWindow(self):

        position_x = 70
        self.create_interface(position_x, 'Baby Monitor')
        self.create_interface(position_x*7.5, 'Smartphone')
        self.create_interface(position_x*15, 'Tv')
        
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
