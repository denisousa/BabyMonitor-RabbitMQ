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
from time import sleep
#from generic_interface import create_interface 

position_x_bm = 70
position_x_smp = position_x_bm * 7.5
position_x_smtv = position_x_bm * 15

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Projecy Babymonitor - IoT"
        self.top = 1000
        self.left = 1000
        self.width = 2000
        self.height = 2000

        self.button_bm = False
        self.button_smp = False
        self.button_smtv = False
        self.button_app = False

        #self.start_thread = False
        self.InitWindow()

    def button_pressed_start(self, device):
        if device == 'baby_monitor':
            baby_monitor_start()
            self.button_bm = True
            thread_bm_data = threading.Thread(target=self.baby_monitor_show_message, args=())
            thread_bm_data.start()

        elif device == 'smartphone':            
            smartphone_start()
            self.button_smp = True
            thread_smp_data = threading.Thread(target=self.smartphone_show_message, args=())
            thread_smp_data.start()

        elif device == 'Tv':
            smart_tv_turn_on()
            self.button_smtv = True  
            self.thread_smtv_data = threading.Thread(target=self.smart_tv_show_message, args=())
            thread_smtv_data.start()

        '''self.connection_bm.setText('<strong>Open connection_bm<\strong>')
        self.connection_bm.setFont(QtGui.QFont('Arial', 12))
        self.connection_bm.adjustSize()
        self.connection_bm.move(70, 550)'''
    
    def button_pressed_stop(self, device):
        if device == 'baby_monitor':
            self.button_bm = False
            baby_monitor_stop()
        elif device == 'smartphone':
            self.button_smp = False
            smartphone_stop()
        elif device == 'Tv':
            self.button_smtv = False
            smartv_turn_off()
            
        ''''self.connection_bm.setText('<strong>Closed connection_bm<\strong>')
        self.connection_bm.setFont(QtGui.QFont('Arial', 12))
        self.connection_bm.adjustSize()
        self.connection_bm.move(70, 550)'''

    def button_pressed_start_app(self, device):
        self.button_app = True
        smart_tv_start_app()

    def button_pressed_stop_app(self, device):
        self.button_app = False
        smart_tv_stop_app()

    def button_pressed_confirm(self):
        smartphone_confirm_notification()
        #data = baby_monitor_get_data()
        #self.button_confirm.setEnabled(False)
        #self.alert.setText("")
        #smartphone_consumer.is_notification = False
        #self.message_confirm.setText("Notification Confirmed")
        #self.message_confirm.setFont(QtGui.QFont('Arial', 12))
        #self.message_confirm.adjustSize()
        #self.message_confirm.move(60, 260) 

    def baby_monitor_show_message(self):
        global position_x_bm
        
        while self.button_bm: 
            data = baby_monitor_get_data()
            self.send_breathing_bm.setText('Breathing: {}'.format(data['breathing']))
            self.send_breathing_bm.setFont(QtGui.QFont('Arial', 12)) 
            self.send_breathing_bm.adjustSize()
            self.send_breathing_bm.move(position_x_bm, 230)

            self.send_time_no_breathing_bm.setText('Time no Breathing: {}'.format(data['time_no_breathing']))
            self.send_time_no_breathing_bm.setFont(QtGui.QFont('Arial', 12)) 
            self.send_time_no_breathing_bm.adjustSize() 
            self.send_time_no_breathing_bm.move(position_x_bm, 250)

            self.send_crying_bm.setText('Crying: {}'.format(data['crying']))
            self.send_crying_bm.setFont(QtGui.QFont('Arial', 12)) 
            self.send_crying_bm.adjustSize() 
            self.send_crying_bm.move(position_x_bm, 270)

            self.send_sleeping_bm.setText('Sleeping: {}'.format(data['sleeping']))
            self.send_sleeping_bm.setFont(QtGui.QFont('Arial', 12)) 
            self.send_sleeping_bm.adjustSize() 
            self.send_sleeping_bm.move(position_x_bm, 290)

            if 'Pending' in baby_monitor_get_confirmation():
                self.pending.setText(baby_monitor_get_confirmation())
                self.pending.setFont(QtGui.QFont('Arial', 12)) 
                self.pending.adjustSize() 
                self.pending.move(position_x_bm, 500)
                self.message_from_smartphone.setText("")
            else:
                self.message_from_smartphone.setText(baby_monitor_get_confirmation())
                self.message_from_smartphone.setFont(QtGui.QFont('Arial', 12)) 
                self.message_from_smartphone.adjustSize() 
                self.message_from_smartphone.move(position_x_bm, 500)
                self.pending.setText("")
                sleep(2)

    def smartphone_show_message(self):
        global position_x_smp
        
        while self.button_smp: 
            data = baby_monitor_get_data()
            self.send_breathing_smp.setText('Breathing: {}'.format(data['breathing']))
            self.send_breathing_smp.setFont(QtGui.QFont('Arial', 12)) 
            self.send_breathing_smp.adjustSize()
            self.send_breathing_smp.move(position_x_smp, 370)

            self.send_time_no_breathing_smp.setText('Time no Breathing: {}'.format(data['time_no_breathing']))
            self.send_time_no_breathing_smp.setFont(QtGui.QFont('Arial', 12)) 
            self.send_time_no_breathing_smp.adjustSize() 
            self.send_time_no_breathing_smp.move(position_x_smp, 390)

            self.send_crying_smp.setText('Crying: {}'.format(data['crying']))
            self.send_crying_smp.setFont(QtGui.QFont('Arial', 12)) 
            self.send_crying_smp.adjustSize() 
            self.send_crying_smp.move(position_x_smp, 410)

            self.send_sleeping_smp.setText('Sleeping: {}'.format(data['sleeping']))
            self.send_sleeping_smp.setFont(QtGui.QFont('Arial', 12)) 
            self.send_sleeping_smp.adjustSize() 
            self.send_sleeping_smp.move(position_x_smp, 430)

            if smartphone_consumer.is_notification:
                if not data['breathing']:
                    txt = "ALERT: Baby Emma isn't breathing!"
                    self.alert.setText(txt)
                    self.alert.setFont(QtGui.QFont('Arial', 12))
                    self.alert.adjustSize()
                    self.alert.move(position_x_smp, 500)
                    self.button_confirm.setEnabled(True)
                
                elif data['crying']:
                    txt = 'ALERT: Baby Emma is crying!'
                    self.alert.setText(txt)
                    self.alert.setFont(QtGui.QFont('Arial', 12))
                    self.alert.adjustSize()
                    self.alert.move(position_x_smp, 500)
                    self.button_confirm.setEnabled(True)
            else:
                txt = ''
                self.alert.setText(txt)
                self.alert.setFont(QtGui.QFont('Arial', 12))
                self.alert.adjustSize()
                self.alert.move(position_x_smp, 500)
                self.button_confirm.setEnabled(False)
                self.message_confirm.setText("")

   
    def smtv_show_message(self):
        global position_x_tv
            
        while self.button_smtv:
            message = smart_tv_get_message()
            txt_status = ''
            if smart_tv_get_status:
                txt_status = 'TV is unblocked.'
            else:
                txt_status = 'TV is blocked.'
            self.information.setText(txt_status)
            if self.button_app:
                self.information.setText('App is running')
            if message: 
                self.receive.setText(message)

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
        self.receive.move(position_x, 340)

        self.information = QLabel(self)
        self.information.setText('<strong>Information<\strong>')
        self.information.setFont(QtGui.QFont('Arial', 14))
        self.information.adjustSize()
        self.information.move(position_x, 470)

        self.connection_bm = QLabel(self)
        self.send_breathing_bm = QLabel(self)
        self.send_time_no_breathing_bm = QLabel(self)
        self.send_crying_bm = QLabel(self)
        self.send_sleeping_bm = QLabel(self)
        self.message_from_smartphone = QLabel(self)
        self.pending = QLabel(self)
        self.connection_smp = QLabel(self)
        self.send_breathing_smp = QLabel(self)
        self.send_time_no_breathing_smp = QLabel(self)
        self.send_crying_smp = QLabel(self)
        self.send_sleeping_smp = QLabel(self)
        self.alert = QLabel(self)

        
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
            self.button = QPushButton('Confirm', self)
            self.button.move(position_x - 20, 640)
            self.button.clicked.connect(self.button_pressed_confirm)
        else:
            self.button = QPushButton('Start', self)
            self.button.move(position_x - 20, 600)
            self.button.clicked.connect(partial(self.button_pressed_start, 'tv'))
            self.button = QPushButton('Stop', self)
            self.button.move(position_x + 100, 600)
            self.button.clicked.connect(partial(self.button_pressed_stop, 'tv'))
            self.button = QPushButton('Start App', self)
            self.button.move(position_x - 20, 640)
            self.button.clicked.connect(self.button_pressed_confirm)
            self.button = QPushButton('Stop App', self)
            self.button.move(position_x + 100, 640)
            self.button.clicked.connect(self.button_pressed_confirm)

   
    def InitWindow(self):

        self.setGeometry(self.top, self.left, self.width, self.height)
        self.create_interface(position_x_bm, 'Baby Monitor')
        self.create_interface(position_x_smp, 'Smartphone')
        self.create_interface(position_x_smtv, 'Tv')
        
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
