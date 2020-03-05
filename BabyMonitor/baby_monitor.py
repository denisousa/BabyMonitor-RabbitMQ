#!/usr/bin/env python
import pika
from time import sleep
import sys
import generate_data as gd
import random
sys.path.append('../')
from construct_scenario import bm, engine
from model_baby_monitor import get_data_baby_monitor

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare exchange of the type 'topic' with name 'exchange_baby_monitor'
channel.exchange_declare(exchange='exchange_baby_monitor', exchange_type='topic')

#Define the route
routing_key = 'baby_monitor_data'

#Define the message
message = 'Hello I am BabyMonitor =)'

for i in range(100):
    print(gd.data_from_baby())
    message = str(get_data_baby_monitor(bm, engine))
    channel.basic_publish(exchange='exchange_baby_monitor', routing_key=routing_key, body=message)

    print(" [x] Sent Topic: %r | Message: %r" % (routing_key, message))
    sleep(2)

connection.close()
