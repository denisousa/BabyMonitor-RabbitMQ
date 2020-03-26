#!/usr/bin/env python
import pika
import sys
import random
sys.path.append('../')
from model_smart_tv import Smart_TV
import threading

smart_tv = Smart_TV()

def smart_tv_turn_on():    
    global smart_tv
    smart_tv.button_is_pressed = True
    smart_tv.start()

def smart_tv_turn_off():
    global smart_tv

    smart_tv.button_is_pressed = False

def smart_tv_start_app():
    global smart_tv

    smart_tv.application = True
    smart_tv.application_thread = threading.Thread(target=smart_tv.aplication_func, args=())
    smart_tv.application_thread.start()

def smart_tv_stop_app():
    global smart_tv

    smart_tv.application = False
    #smart_tv.application_thread = threading.Thread(target=self.aplication_func, args=())
    smart_tv.status = True
    
def smart_tv_get_status():
    global smart_tv

    return smart_tv.status

def smart_tv_get_application():
    global smart_tv

    return smart_tv.application

def smart_tv_get_message():
    global smart_tv

    return smart_tv.message