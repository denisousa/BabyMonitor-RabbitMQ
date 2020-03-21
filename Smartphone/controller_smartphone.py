#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_smartphone import Smartphone

smartphone_producer = Smartphone()
smartphone_consumer = Smartphone()

#start conection
def start():
    global smartphone_producer, smartphone_consumer

    smartphone_consumer.is_consumer = True


    
#stop conection
def stop():
	smartphone.button_is_pressed = False

#get data from db
def get_data():
	smartphone.get_data_baby_monitor()

def confirm_notification():
    smartphone.forward_to_tv()