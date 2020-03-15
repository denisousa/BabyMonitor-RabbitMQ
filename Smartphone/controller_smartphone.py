#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_smartphone import Smartphone

smartphone = Smartphone()

#start conection
def start():
    global smartphone
    smartphone = Smartphone()
    smartphone.button_is_pressed = True
    smartphone.start()

#stop conection
def stop():
	smartphone.button_is_pressed = False

#get data from db
def get_data():
	smartphone.get_data_baby_monitor()	

def confirm_notification():
    pass