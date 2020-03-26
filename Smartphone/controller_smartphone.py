#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_smartphone import SmartphoneConsumer, SmartphoneProducer

smartphone_consumer = SmartphoneConsumer()

#start conection
def smartphone_start():
	global smartphone_consumer
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
	global smartphone_consumer

	smartphone_producer = SmartphoneProducer()
	if smartphone_consumer.is_notification:
		smartphone_producer.button_is_pressed = True
		#smartphone_producer = SmartphoneProducer()
		smartphone_producer.start()
		smartphone_consumer.is_notification = False

def smartphone_get_notfication():
	global smartphone_consumer

	#print(f'from controller: {smartphone_consumer.is_notification}')
	return smartphone_consumer.is_notification