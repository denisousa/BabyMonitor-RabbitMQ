#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_baby_monitor import Baby_Monitor, notif_confirm

monitor_producer = Baby_Monitor()
monitor_consumer = Baby_Monitor()
    
#start conection
def start():
    global monitor_producer, monitor_consumer

    monitor_consumer.is_consumer = True
    monitor_consumer.start()

    monitor_producer.is_producer = True
    monitor_producer.button_is_pressed = True
    monitor_producer.start()      
    
#stop conection
def stop():
    global monitor_producer

    monitor_producer.button_is_pressed = False

#get data from db
def get_data():
    global monitor_producer

    return monitor_producer.get_data_baby_monitor()

def get_confirmation():
    if notif_confirm[0]:
        if notif_confirm[1]:
            return 'Confirmation received.'
        else:
            return 'Pending notification.'
    else:
        return ''
