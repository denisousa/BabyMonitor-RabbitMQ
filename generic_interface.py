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

def baby_monitor_show_message(self):
    global position_x
    
    while self.button_bm: 
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