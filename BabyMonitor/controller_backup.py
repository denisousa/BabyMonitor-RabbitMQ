#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_baby_monitor import Baby_Monitor, notif_confirm

monitor = Baby_Monitor()
    
#start conection
def start():
    global monitor

    monitor.button_is_pressed = True
    monitor.start()      
    
#stop conection
def stop():
    global monitor

    monitor.button_is_pressed = False

#get data from db
def get_data():
    global monitor

    return monitor.get_data_baby_monitor()

def get_confirmation():
    if notif_confirm[0]:
        if notif_confirm[1]:
            return 'Confirmation received.'
        else:
            return 'Pending notification.'
    else:
        return ''
