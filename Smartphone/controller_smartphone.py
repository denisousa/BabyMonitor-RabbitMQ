#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from model_smartphone import SmartphoneConsumer, SmartphoneProducer
import textwrap
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

def smartphone_confirm_notification():
	global smartphone_consumer
	smartphone_producer = None
	
	if smartphone_consumer.is_notification:
		smartphone_producer = SmartphoneProducer()
		smartphone_producer.button_is_pressed = True
		smartphone_consumer.is_notification = False
		smartphone_producer.start()

def smartphone_get_notfication():
	global smartphone_consumer
	return smartphone_consumer.is_notification

def smartphone_get_message():
	global smartphone_consumer

	message = smartphone_consumer.message
	if '{' in message:
		return eval(message)

	message = message.replace('b"','')
	message = message.replace('"', '')

	return message