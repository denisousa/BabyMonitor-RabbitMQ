#!/usr/bin/env python
import pika
import sys
import random
sys.path.append('../')
from construct_scenario import queue_smartv, routing_key_smart_tv, exchange_baby_monitor


#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_bind(
        exchange=exchange_baby_monitor, queue=queue_smartv, routing_key=routing_key_smart_tv)

status = False

def generate_status():
    return random.choices([True, False], [0.50,0.50], k=1)[0]

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    status = generate_status() 
    print(status)
    if status:
        print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
    else:
        print(" [x] Receive Topic: %r | Message: Smart Tv blocked!!" % (method.routing_key))

channel.basic_consume(
    queue=queue_smartv, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
