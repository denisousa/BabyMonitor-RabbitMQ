#!/usr/bin/env python
import pika
from time import sleep
import sys
import generate_data as gd
import random

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare exchange of the type 'topic' with name 'exchange_baby_monitor'
channel.exchange_declare(exchange='exchange_baby_monitor', exchange_type='topic')

#Define the route
routing_key = 'baby_monitor_data'

#Degine the message
message = 'Hello I am BabyMonitor =)'

#Publish in the channel
count = 0
maxNoChanges = random.randint(5, 8)
for i in range(100):
    message = str(gd.data_from_baby(count))
    channel.basic_publish(
        exchange='exchange_baby_monitor', routing_key=routing_key, body=message)
    print(" [x] Sent Topic: %r | Message: %r" % (routing_key, message))
    sleep(2)

    if count <= maxNoChanges: 
        count += 1
    else: 
        count = 0 
        maxNoChanges = random.randint(5,8)
        print('changes ', maxNoChanges)

connection.close()
