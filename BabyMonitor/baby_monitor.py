#!/usr/bin/env python
import pika
from time import sleep
import sys
from generate_data import data_from_baby
import random
sys.path.append('../')
from construct_scenario import bm, engine, routing_key_smartphone
from model_baby_monitor import get_data_baby_monitor

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Sends the message
for i in range(100):
    data_from_baby()

    line = get_data_baby_monitor(bm, engine)

    keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')

    message = str(dict(zip(keys, line)))
    channel.basic_publish(exchange='exchange_baby_monitor', routing_key=routing_key_smartphone, body=message)

    print(" [x] Sent Topic: %r | Message: %r" % (routing_key_smartphone, message))
    sleep(2)

connection.close()
