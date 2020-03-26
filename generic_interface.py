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

def create_interface(object_interface, position_x, name_interface):
    # Define title device
    object_interface.title_baby_monitor = QLabel(object_interface)
    object_interface.title_baby_monitor.setText('<strong>{}<\strong>'.format(name_interface))
    object_interface.title_baby_monitor.setFont(QtGui.QFont('Arial', 16))
    object_interface.title_baby_monitor.adjustSize()
    object_interface.title_baby_monitor.move(position_x, 10)

    object_interface.send = QLabel(object_interface)
    object_interface.send.setText('<strong>Send<\strong>')
    object_interface.send.setFont(QtGui.QFont('Arial', 14))
    object_interface.send.adjustSize()
    object_interface.send.move(position_x, 200)

    object_interface.receive = QLabel(object_interface)
    object_interface.receive.setText('<strong>Receive<\strong>')
    object_interface.receive.setFont(QtGui.QFont('Arial', 14))
    object_interface.receive.adjustSize()
    object_interface.receive.move(position_x, 320)

    object_interface.information = QLabel(object_interface)
    object_interface.information.setText('<strong>Information<\strong>')
    object_interface.information.setFont(QtGui.QFont('Arial', 14))
    object_interface.information.adjustSize()
    object_interface.information.move(position_x, 420)

    object_interface.connection = QLabel(object_interface)
    object_interface.send_breathing = QLabel(object_interface)
    object_interface.send_time_no_breathing = QLabel(object_interface)
    object_interface.send_crying = QLabel(object_interface)
    object_interface.send_sleeping = QLabel(object_interface)
    object_interface.message_from_smartphone = QLabel(object_interface)
    object_interface.pending = QLabel(object_interface)
    
    if name_interface == 'Baby Monitor':
        object_interface.send_breathing.setFont(QtGui.QFont('Arial', 12)) 
        object_interface.send_breathing.adjustSize()
        object_interface.send_breathing.move(70, 230)

        object_interface.send_time_no_breathing.setFont(QtGui.QFont('Arial', 12)) 
        object_interface.send_time_no_breathing.adjustSize() 
        object_interface.send_time_no_breathing.move(70, 250)

        object_interface.send_crying.setFont(QtGui.QFont('Arial', 12)) 
        object_interface.send_crying.adjustSize() 
        object_interface.send_crying.move(70, 270)

        object_interface.send_sleeping.setFont(QtGui.QFont('Arial', 12)) 
        object_interface.send_sleeping.adjustSize() 
        object_interface.send_sleeping.move(70, 290)

        object_interface.pending.setFont(QtGui.QFont('Arial', 12)) 
        object_interface.pending.adjustSize() 
        object_interface.pending.move(70, 460)
        object_interface.message_from_smartphone.setText("")

        object_interface.message_from_smartphone.setText(baby_monitor_get_confirmation())
        object_interface.message_from_smartphone.setFont(QtGui.QFont('Arial', 12)) 
        object_interface.message_from_smartphone.adjustSize() 
        object_interface.message_from_smartphone.move(70, 460)

        object_interface.button = QPushButton('Start', object_interface)
        object_interface.button.move(position_x - 20, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_start, 'baby_monitor'))
        object_interface.button = QPushButton('Stop', object_interface)
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'baby_monitor'))
    
    elif name_interface == 'Smartphone':
        object_interface.button = QPushButton('Start', object_interface)
        object_interface.button.move(position_x - 20, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_start, 'smartphone'))
    
        object_interface.button = QPushButton('Stop', object_interface)
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'smartphone'))
    
        '''object_interface.button_confirm = QPushButton('Confirm', object_interface)
        object_interface.button_confirm.setEnabled(False)
        object_interface.button_confirm.move(740, 600)
        object_interface.button_confirm.clicked.connect(object_interface.button_pressed_confirm)'''
    
    else:
        object_interface.button = QPushButton('Start', object_interface)
        object_interface.button.move(position_x - 20, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_start, 'tv'))
        object_interface.button = QPushButton('Stop', object_interface)
        object_interface.button.move(position_x + 100, 600)
        object_interface.button.clicked.connect(partial(object_interface.button_pressed_stop, 'tv'))