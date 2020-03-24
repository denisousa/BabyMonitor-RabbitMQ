#!/usr/bin/env python
import pika
import sys
import random
sys.path.append('../')
from construct_scenario import queue_smart_tv, routing_key_smart_tv, exchange_baby_monitor
from model_smart_tv import Smart_TV
import threading

smart_tv = Smart_TV()


def turn_on():    
    global smart_tv
    smart_tv.button_is_pressed = True
    smart_tv.start()

def turn_off():
    global smart_tv

    smart_tv.button_is_pressed = False

def start_app():
    global smart_tv

    smart_tv.application = True
    smart_tv.application_thread.start()

def stop_app():
    global smart_tv

    smart_tv.application = False
    #smart_tv.application_thread = threading.Thread(target=self.aplication_func, args=())
    smart_tv.status = True
    