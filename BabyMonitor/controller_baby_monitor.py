#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_baby_monitor import BabyMonitorConsumer, BabyMonitorProducer, notif_confirm
import threading

monitor_producer = BabyMonitorProducer()
monitor_consumer = BabyMonitorConsumer()

#start conection
def baby_monitor_start():
    global monitor_producer, monitor_producer

    monitor_producer = BabyMonitorProducer()
    monitor_consumer = BabyMonitorConsumer()

    monitor_producer.button_is_pressed = True
    monitor_consumer.button_is_pressed = True
    
    monitor_consumer.start()
    monitor_producer.start()      
    

#stop conection
def baby_monitor_stop():
    global monitor_producer, monitor_consumer

    monitor_producer.button_is_pressed = False
    monitor_consumer.button_is_pressed = False
    #monitor_consumer.join()
    #monitor_producer.join()

#get data from db
def baby_monitor_get_data():
    global monitor_producer

    return monitor_producer.message

def baby_monitor_get_confirmation():
    if notif_confirm[0]:
        if notif_confirm[1]:
            return 'Confirmation received.'
        else:
            return 'Pending notification.'
    else:
        return ''

def baby_monitor_get_status():
    global monitor_producer

    return monitor_producer.get_data_baby_monitor()