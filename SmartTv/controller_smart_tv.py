#!/usr/bin/env python
import pika
import sys
import random
sys.path.append('../')
from construct_scenario import queue_smart_tv, routing_key_smart_tv, exchange_baby_monitor
from model_smart_tv import SmartTV
import threading

smart_tv = SmartTV()


def smart_tv_turn_on():    
    global smart_tv
    smart_tv.button_is_pressed = True
    smart_tv.start_connection()

def smart_tv_turn_off():
    global smart_tv

    smart_tv.button_is_pressed = False

def smart_tv_start_app():
    global smart_tv

    smart_tv.application = True
    smart_tv.application_thread.start()

def smart_tv_stop_app():
    global smart_tv

    smart_tv.application = False
    smart_tv.status = True
    
def smart_tv_get_status():
    global smart_tv

    return smart_tv.status

def smart_tv_get_message():
    global smart_tv

    return smart_tv.message_received