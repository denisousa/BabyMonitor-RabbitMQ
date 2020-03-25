#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_smartphone import Smartphone

smartphone_consumer = Smartphone()

#start conection
def smartphone_start():
	global smartphone_producer, smartphone_consumer

	smartphone_consumer.is_consumer = True
	smartphone_consumer.button_is_pressed = True
	smartphone_consumer.start()
	
#stop conection
def smartphone_stop():
	global smartphone_consumer
	smartphone_consumer.button_is_pressed = False

#get data from db
def smartphone_get_data():
	global smartphone_consumer

	return smartphone_consumer.get_data_baby_monitor()

def smartphone_confirm_notification():
	global smartphone_producer

	smartphone_producer = Smartphone()
	smartphone_producer.button_is_pressed = True
	smartphone_producer.is_producer = True
	smartphone_producer.start()
	'''if smartphone_consumer.is_notification:
		smartphone_consumer.is_notification = False
		smartphone_producer.button_is_pressed = True'''