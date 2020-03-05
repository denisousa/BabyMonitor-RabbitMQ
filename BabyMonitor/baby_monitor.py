#!/usr/bin/env python
import pika
from time import sleep
import sys
from generate_data import data_from_baby
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

#Sends the message
for i in range(100):
    data_from_baby()

    line = get_data_baby_monitor(bm, engine)

    keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')

    message = str(dict(zip(keys, line)))
    channel.basic_publish(exchange='exchange_baby_monitor', routing_key=routing_key, body=message)

    print(" [x] Sent Topic: %r | Message: %r" % (routing_key, message))
    sleep(2)

connection.close()
