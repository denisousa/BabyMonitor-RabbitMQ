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
from generic_interface import *

class Window(QMainWindow):                                                                                                                                          
    def __init__(self):
        super().__init__()

        self.title = "Babymonitor Project - IoT"
        self.top = 1000
        self.left = 1000
        self.width = 2000
        self.height = 2000
        
        self.button_bm = False
        self.button_smp = False
        self.button_smtv = False
        
        self.thread_babymonitor_data = False
        self.thread_smartphone_data = False
        self.thread_smarttv_data = False
        
        self.InitWindow()

    def button_pressed_start(self, device):
        
        if device == 'baby_monitor':
            baby_monitor_start()
            self.button_bm = True
            self.thread_babymonitor_data = threading.Thread(target=self.baby_monitor_show_message, args=())
            self.thread_babymonitor_data.start()
        
        elif device == 'smartphone':
            smartphone_start()
            self.button_smp = True #usar o mesmo self.button pra todo não dá problema?
            self.thread_smartphone_data = threading.Thread(target=self.smartphone_show_message, args=())
            self.thread_smartphone_data.start()
        
        elif device == 'Tv':
            smart_tv_turn_on()
            self.button_smtv = True  
            self.thread_smarttv_data = threading.Thread(target=self.smart_tv_show_message, args=())

        self.connection.setText('<strong>Open connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 12))
        self.connection.adjustSize()
        self.connection.move(70, 550)
    
    def button_pressed_stop(self, device):
        
        if device == 'baby_monitor':
            self.button = False
            self.thread_babymonitor_data = False
            baby_monitor_stop()
        elif device == 'smartphone':
            pass
        else:
            pass
        self.connection.setText('<strong>Closed connection<\strong>')
        self.connection.setFont(QtGui.QFont('Arial', 12))
        self.connection.adjustSize()
        self.connection.move(70, 550)


    def smartphone_show_message(self):
        global position_x

        while self.button_smp:
            data = smartphone_get_data()
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

    def smart_tv_show_message(self):
        global position_x

        while self.button_smtv:
            message = smart_tv_get_message()

    def baby_monitor_show_message(self):
        global position_x
        while self.button_bm: 
            data = baby_monitor_get_data()
            self.send_breathing.setText('Breathing: {}'.format(data['breathing']))

            self.send_time_no_breathing.setText('Time no Breathing: {}'.format(data['time_no_breathing']))

            self.send_crying.setText('Crying: {}'.format(data['crying']))

            self.send_sleeping.setText('Sleeping: {}'.format(data['sleeping']))

            if 'Pending' in baby_monitor_get_confirmation():
                self.pending.setText(baby_monitor_get_confirmation())
            else:
                self.pending.setText("")

    def InitWindow(self):

        position_x = 70
        create_interface(self, position_x, 'Baby Monitor')
        create_interface(self, position_x*7.5, 'Smartphone')
        create_interface(self, position_x*15, 'Tv')
        
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
        
        self.show()