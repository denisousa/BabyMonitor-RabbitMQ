#!/usr/bin/env python
import pika
import sys

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue_baby_monitor = 'queue_baby_monitor'
queue_smartphone = 'queue_smartphone'
exchange_baby_monitor = 'exchange_baby_monitor'

#Declare exchange of the type 'topic' with name 'exchange_baby_monitor'
channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type='topic')
channel.queue_declare(queue_baby_monitor, exclusive=True)
channel.queue_declare(queue_smartphone, exclusive=True)

print('Built Scenario...')

while True:
    pass