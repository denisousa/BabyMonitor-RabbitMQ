#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_baby_monitor import BabyMonitorConsumer, BabyMonitorProducer, notif_confirm

monitor_producer = BabyMonitorProducer()
monitor_consumer = BabyMonitorConsumer()

#start conection
def baby_monitor_start():
    global monitor_producer, monitor_producer

    monitor_producer = BabyMonitorProducer()
    monitor_consumer = BabyMonitorConsumer()

    monitor_producer.button_is_pressed = True
    monitor_consumer.button_is_pressed = True
    
    monitor_producer.start()      
    monitor_consumer.start()

#stop conection
def baby_monitor_stop():
    global monitor_producer, monitor_consumer

    monitor_producer.button_is_pressed = False
    monitor_consumer.button_is_pressed = False

#get data from db
def baby_monitor_get_data():
    global monitor_consumer

    return monitor_consumer.get_data_baby_monitor()

def baby_monitor_get_confirmation():
    if notif_confirm[0]:
        if notif_confirm[1]:
            return 'Confirmation received.'
        else:
            return 'Pending notification.'
    else:
        return ''