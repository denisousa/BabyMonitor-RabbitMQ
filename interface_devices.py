from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5 import QtGui
from PyQt5 import QtCore
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
from observer import main
#from generic_interface import create_interface 

position_x_bm = 70
position_x_smp = position_x_bm * 5
position_x_smtv = position_x_bm * 9

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Project Babymonitor - IoT"
        self.top = 1000
        self.left = 1000
        self.width = 2000
        self.height = 2000

        self.button_bm = False
        self.button_smp = False
        self.button_smtv = False
        self.button_smp_confirm = False

        self.is_adapted = False

        self.InitWindow()

    def start_middleware(self):
        main(self.is_adapted)


    def button_pressed_start(self, device):
        global position_x_bm, position_x_smp, position_x_smtv
        
        if device == 'baby_monitor':
            baby_monitor_start()
            self.button_bm = True
            thread_bm_data = threading.Thread(target=self.baby_monitor_show_message, args=())
            thread_bm_data.start()
            self.connection_bm.setText('<strong>Open connection Baby Monitor<\strong>')
            self.connection_bm.setFont(QtGui.QFont('Arial', 12))
            self.connection_bm.adjustSize()
            self.connection_bm.move(position_x_bm, 550)
            
            start_emma = threading.Thread(target=self.show_status_emma, args=())
            start_emma.start()

        elif device == 'smartphone':            
            smartphone_start()
            self.button_smp = True
            thread_smp_data = threading.Thread(target=self.smartphone_show_message, args=())
            thread_smp_data.start()

            self.connection_smp.setText('<strong>Open connection Smartphone<\strong>')
            self.connection_smp.setFont(QtGui.QFont('Arial', 12))
            self.connection_smp.adjustSize()
            self.connection_smp.move(position_x_smp, 550)

        elif device == 'tv':
            print('HEAR')
            smart_tv_turn_on()
            print('HEAR AFTER')
            self.button_smtv = True  
            thread_smtv_data = threading.Thread(target=self.smart_tv_show_message, args=())
            thread_smtv_data.start()

            self.connection_smtv.setText('<strong>Open connection Smart TV<\strong>')
            self.connection_smtv.setFont(QtGui.QFont('Arial', 12))
            self.connection_smtv.adjustSize()
            self.connection_smtv.move(position_x_smtv, 550)
            print('HEAR')

        self.adaptation.setEnabled(False)
        self.start_middleware()
    
    def button_pressed_stop(self, device):
        if device == 'baby_monitor':
            self.button_bm = False
            baby_monitor_stop()
            self.connection_bm.setText('<strong>Closed connection Baby Monitor<\strong>')
            self.connection_bm.setFont(QtGui.QFont('Arial', 12))
            self.connection_bm.adjustSize()
            self.connection_bm.move(position_x_bm, 550)

        elif device == 'smartphone':
            self.button_smp = False
            smartphone_stop()
            self.connection_smp.setText('<strong>Closed connection Smartphone<\strong>')
            self.connection_smp.setFont(QtGui.QFont('Arial', 12))
            self.connection_smp.adjustSize()
            self.connection_smp.move(position_x_smp, 550)

        elif device == 'tv':
            self.button_smtv = False
            smar_tv_turn_off()
            self.connection_smtv.setText('<strong>Closed connection Smart TV<\strong>')
            self.connection_smtv.setFont(QtGui.QFont('Arial', 12))
            self.connection_smtv.adjustSize()
            self.connection_smtv.move(position_x_smtfv, 550)

    def button_pressed_start_app(self, device):
        smart_tv_start_app()

    def button_pressed_stop_app(self, device):
        smart_tv_stop_app()

    def button_pressed_confirm(self):
        smartphone_confirm_notification()
        data = baby_monitor_get_data()
        self.button_smp_confirm = True
        self.button_confirm.setEnabled(False)
        sleep(1)

        '''self.alert.setText("")
        smartphone_consumer.is_notification = False
        self.message_confirm.setText("Notification Confirmed")
        self.message_confirm.setFont(QtGui.QFont('Arial', 12))
        self.message_confirm.adjustSize()
        self.message_confirm.move(500, 500)
        sleep(2)
        self.message_confirm.setText('')'''

    def check_adaptation(self, state):
        if state == QtCore.Qt.Checked:        
            self.is_adapted = True
        else: 
            self.is_adapted = False

    def baby_monitor_show_message(self):
        global position_x_bm

        while self.button_bm:

            data = baby_monitor_get_data()
            if data:
                if 'STATUS' in data:
                    data = data.replace('STATUS: ', '')
                    data = eval(data)
                    print(f'HEAR: {data}') 
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

                    self.notification_bm.setText("")
                    self.notification_bm.setWordWrap(False)
                    self.notification_bm.adjustSize()
                else:
                    self.send_breathing_bm.setText('')
                    self.send_sleeping_bm.setText('')
                    self.send_crying_bm.setText('')
                    self.send_time_no_breathing_bm.setText('')
                    self.notification_bm.setFixedWidth(150)
                    self.notification_bm.setWordWrap(True)
                    self.notification_bm.setFont(QtGui.QFont('Arial', 12))
                    self.notification_bm.adjustSize()
                    self.notification_bm.move(position_x_bm, 230)
                    self.notification_bm.setText(data.replace('NOTIFICATION', 'Notification'))

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

                sleep(1)

    def smartphone_show_message(self):
        global position_x_smp
        
        while self.button_smp:
            data = smartphone_get_message()
            if isinstance(data, dict):
                self.receive_breathing_smp.setText('Breathing: {}'.format(data['breathing']))
                self.receive_breathing_smp.setFont(QtGui.QFont('Arial', 12)) 
                self.receive_breathing_smp.adjustSize()
                self.receive_breathing_smp.move(position_x_smp, 370)

                self.receive_time_no_breathing_smp.setText('Time no Breathing: {}'.format(data['time_no_breathing']))
                self.receive_time_no_breathing_smp.setFont(QtGui.QFont('Arial', 12)) 
                self.receive_time_no_breathing_smp.adjustSize() 
                self.receive_time_no_breathing_smp.move(position_x_smp, 390)

                self.receive_crying_smp.setText('Crying: {}'.format(data['crying']))
                self.receive_crying_smp.setFont(QtGui.QFont('Arial', 12)) 
                self.receive_crying_smp.adjustSize() 
                self.receive_crying_smp.move(position_x_smp, 410)

                self.receive_sleeping_smp.setText('Sleeping: {}'.format(data['sleeping']))
                self.receive_sleeping_smp.setFont(QtGui.QFont('Arial', 12)) 
                self.receive_sleeping_smp.adjustSize()
                self.receive_sleeping_smp.move(position_x_smp, 430)

                self.alert.setText("Everything's fine :)")
                self.alert.setFont(QtGui.QFont('Arial', 12))
                self.alert.adjustSize()
                self.alert.move(position_x_smp, 500)

                self.notification.setText("")
                self.notification.setWordWrap(False)
                self.notification.adjustSize()

                self.send_confirmation_smp.setText("")
                self.button_smp_confirm = False
                #self.button_confirm.setEnabled(False)

            else:
                self.notification.setFixedWidth(150)
                self.notification.setWordWrap(True)
                self.notification.setFont(QtGui.QFont('Arial', 12))
                self.notification.adjustSize()
                self.notification.move(position_x_smp, 370)
                self.notification.setText(data.replace('NOTIFICATION', 'Notification'))

                self.receive_breathing_smp.setText('')
                self.receive_time_no_breathing_smp.setText('')
                self.receive_crying_smp.setText('')
                self.receive_sleeping_smp.setText('')
                self.alert.setText("")
                
            if self.button_smp_confirm:
                self.send_confirmation_smp.setText('Confirmation Sent.')
                self.send_confirmation_smp.setFont(QtGui.QFont('Arial', 12)) 
                self.send_confirmation_smp.adjustSize() 
                self.send_confirmation_smp.move(position_x_smp, 240)
            else:
                self.send_confirmation_smp.setText('')

            if smartphone_get_notification():
                self.button_confirm.setEnabled(True)
            else:
                self.button_confirm.setEnabled(True)
            
    def smart_tv_show_message(self):
        global position_x_tv
            
        while self.button_smtv:
            if smart_tv_get_status():
                self.status_smtv.setText('TV is unlocked')
                self.status_smtv.setFont(QtGui.QFont('Arial', 12)) 
                self.status_smtv.adjustSize()
                self.status_smtv.move(position_x_smtv, 500)
            else:
                self.status_smtv.setText('TV is locked')
                self.status_smtv.setFont(QtGui.QFont('Arial', 12)) 
                self.status_smtv.adjustSize()
                self.status_smtv.move(position_x_smtv, 500)
                self.receive_message_smtv.setText('')

            if smart_tv_get_application():
                self.app_smtv.setText('App is running')
                self.app_smtv.setFont(QtGui.QFont('Arial', 12)) 
                self.app_smtv.adjustSize()
                self.app_smtv.move(position_x_smtv, 520)
                self.receive_message_smtv.setText('')
            
            else:
                self.app_smtv.setText('No app running')
                self.app_smtv.setFont(QtGui.QFont('Arial', 12)) 
                self.app_smtv.adjustSize()
                self.app_smtv.move(position_x_smtv, 520)

            data = smart_tv_get_message()
            
            self.receive_message_smtv.setFixedWidth(150)
            self.receive_message_smtv.setWordWrap(True)

            self.receive_message_smtv.setFont(QtGui.QFont('Arial', 12)) 
            self.receive_message_smtv.adjustSize()
            self.receive_message_smtv.move(position_x_smtv, 370)
            
            if data == '':
                self.receive_message_smtv.setText('')
            else:
                self.receive_message_smtv.setText(data.replace('NOTIFICATION', 'Notification'))
                
    def show_status_emma(self):	
        while self.button_bm:
            check_ = baby_monitor_get_status()
            self.status_breathing.setText('Breathing: {}'.format(check_['breathing']))
            self.status_breathing.setFont(QtGui.QFont('Arial', 12)) 
            self.status_breathing.adjustSize()
            self.status_breathing.move(position_x_smtv + 310, 430)

            self.status_time_no_breathing.setText('Time no Breathing: {}'.format(check_['time_no_breathing']))
            self.status_time_no_breathing.setFont(QtGui.QFont('Arial', 12)) 
            self.status_time_no_breathing.adjustSize() 
            self.status_time_no_breathing.move(position_x_smtv + 310, 450)

            self.status_crying.setText('Crying: {}'.format(check_['crying']))
            self.status_crying.setFont(QtGui.QFont('Arial', 12)) 
            self.status_crying.adjustSize() 
            self.status_crying.move(position_x_smtv + 310, 470)

            self.status_sleeping.setText('Sleeping: {}'.format(check_['sleeping']))
            self.status_sleeping.setFont(QtGui.QFont('Arial', 12)) 
            self.status_sleeping.adjustSize() 
            self.status_sleeping.move(position_x_smtv + 310, 490)

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
        self.image_bm = QLabel(self)
        
        self.connection_smp = QLabel(self)
        self.receive_breathing_smp = QLabel(self)
        self.receive_time_no_breathing_smp = QLabel(self)
        self.receive_crying_smp = QLabel(self)
        self.receive_sleeping_smp = QLabel(self)
        self.send_confirmation_smp = QLabel(self)
        self.alert = QLabel(self)
        self.image_smp = QLabel(self)

        self.connection_smtv = QLabel(self)
        self.notification_bm = QLabel(self)

        self.notification = QLabel(self)
        self.status_smtv = QLabel(self)
        self.app_smtv = QLabel(self)
        self.receive_message_smtv = QLabel(self)
        self.image_smtv = QLabel(self)

        if name_interface == 'Baby Monitor':
            self.button_start = QPushButton('Start', self)
            self.button_start.move(position_x - 20, 600)
            self.button_start.clicked.connect(partial(self.button_pressed_start, 'baby_monitor'))
            self.button_stop = QPushButton('Stop', self)
            self.button_stop.move(position_x + 100, 600)
            self.button_stop.clicked.connect(partial(self.button_pressed_stop, 'baby_monitor'))
        
        elif name_interface == 'Smartphone':
            self.button_start = QPushButton('Start', self)
            self.button_start.move(position_x - 20, 600)
            self.button_start.clicked.connect(partial(self.button_pressed_start, 'smartphone'))
            self.button_stop = QPushButton('Stop', self)
            self.button_stop.move(position_x + 100, 600)
            self.button_stop.clicked.connect(partial(self.button_pressed_stop, 'smartphone'))
            self.button_confirm = QPushButton('Confirm', self)
            self.button_confirm.move(position_x - 20, 640)
            self.button_confirm.clicked.connect(self.button_pressed_confirm)
            self.button_confirm.setEnabled(False)
        else:
            self.button_start = QPushButton('Start', self)
            self.button_start.move(position_x - 20, 600)
            self.button_start.clicked.connect(partial(self.button_pressed_start, 'tv'))
            self.button_stop = QPushButton('Stop', self)
            self.button_stop.move(position_x + 100, 600)
            self.button_stop.clicked.connect(partial(self.button_pressed_stop, 'tv'))
            self.button_start_app = QPushButton('Start App', self)
            self.button_start_app.move(position_x - 20, 640)
            self.button_start_app.clicked.connect(self.button_pressed_start_app)
            self.button_stop_app = QPushButton('Stop App', self)
            self.button_stop_app.move(position_x + 100, 640)
            self.button_stop_app.clicked.connect(self.button_pressed_stop_app)

   
    def InitWindow(self):
        global position_x_bm, position_x_smp, position_x_smtv

        self.status_breathing = QLabel(self)
        self.status_time_no_breathing = QLabel(self)
        self.status_sleeping = QLabel(self)
        self.status_crying = QLabel(self)

        self.setGeometry(self.top, self.left, self.width, self.height)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("./imgs/babymonitor.png"))
        self.label.setGeometry(position_x_bm + 10, 10, 200, 200)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("./imgs/smartphone.png"))
        self.label.setGeometry(position_x_smp + 10, 60, 100, 100)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("./imgs/monitor.svg"))
        self.label.setGeometry(position_x_smtv - 10, 10, 200, 200)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("./imgs/emma.png"))
        self.label.setGeometry(position_x_smtv + 280, 200, 200, 200)

        self.create_interface(position_x_bm, 'Baby Monitor')
        self.create_interface(position_x_smp, 'Smartphone')
        self.create_interface(position_x_smtv, 'Smart Tv')
        self.setWindowIcon(QtGui.QIcon("./imgs/babymonitor.png"))

        self.title_device = QLabel(self)
        self.title_device.setText('<strong>BabyMonitor - IoT<\strong>')
        self.title_device.setFont(QtGui.QFont('Arial', 30)) 
        self.title_device.adjustSize()
        self.title_device.move(position_x_smtv + 200, 80)

        self.adaptation = QCheckBox('Cautious adaptation?', self)
        self.adaptation.setFont(QtGui.QFont('Arial', 12)) 
        self.adaptation.adjustSize()
        self.adaptation.stateChanged.connect(self.check_adaptation)
        self.adaptation.move(position_x_smtv + 280, 150)
        
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
