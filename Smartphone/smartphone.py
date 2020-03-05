#!/usr/bin/env python
import pika
import sys
import random

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue_baby_monitor = 'queue_baby_monitor'
queue_smartphone = 'queue_smartphone'
routing_key_one = 'baby_monitor_data'
routing_key_second = 'smart_tv_data'
exchange_baby_monitor = 'exchange_baby_monitor'

#Declare exchange of the type 'topic' with name 'exchange_baby_monitor'
channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type='topic')
channel.queue_declare(queue_baby_monitor, exclusive=True)
channel.queue_declare(queue_smartphone, exclusive=True)

channel.queue_bind(
        exchange=exchange_baby_monitor, queue=queue_baby_monitor, routing_key=routing_key_one)

channel.queue_bind(
        exchange=exchange_baby_monitor, queue=queue_smartphone, routing_key=routing_key_second)


print(' [*] Waiting for messages. To exit press CTRL+C')

def forward_to_tv(message):
    channel.basic_publish(exchange='exchange_smart_tv', routing_key=routing_key_second, body=message)

def read_message(message):
    message = eval(message)
    if not message['breathing'] and message['time_no_breathing'] > 3:
        print("ALERT! Emma isn't breathing")    #criar método notificação para mostrar na view
        delay = random.randint(1, 5)
        if delay >= 3: 
            print('Forwarding to TV')
            forward_to_tv(str(message))

def callback(ch, method, properties, body):
    print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
    read_message(body)
    

channel.basic_consume(
    queue=queue_baby_monitor, on_message_callback=callback, auto_ack=True)

channel.basic_consume(
    queue=queue_smartphone, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
