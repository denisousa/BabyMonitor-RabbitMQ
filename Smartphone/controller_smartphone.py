#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from construct_scenario import main.*
from model_smartphone import *

smartphone = Smartphone()

def start():
    global smartphone
    print('I was called')
    smartphone.button_is_pressed = True
    smartphone.start()

def stop():
	smartphone.button_is_pressed = False

def get_data():
	global smartphone
	smartphone.get_data_baby_monitor()	

def confirm_notification():
    pass