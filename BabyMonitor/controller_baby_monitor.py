#!/usr/bin/env python
import pika
from time import sleep
import sys
sys.path.append('../')
from construct_scenario import engine, meta
from model_baby_monitor import Baby_Monitor

monitor = None

#start conection
def start():
    global monitor
    monitor = Baby_Monitor()
    monitor.button_is_pressed = True
    monitor.start()      
    
#stop conection
def stop():
    monitor.button_is_pressed = False

#get data from db
def get_data():
    return monitor.get_data_baby_monitor()
    