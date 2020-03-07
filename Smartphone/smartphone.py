#!/usr/bin/env python
import pika
import sys
import random
import sys
sys.path.append('../')
from construct_scenario import queue_smartphone, queue_smartv, routing_key_smart_tv, routing_key_smartphone, exchange_baby_monitor

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_bind(
        exchange='exchange_baby_monitor', queue=queue_smartphone, routing_key=routing_key_smartphone)

channel.queue_bind(
        exchange='exchange_baby_monitor', queue=queue_smartv, routing_key=routing_key_smart_tv)


print(' [*] Waiting for messages. To exit press CTRL+C')

def forward_to_tv(message):
    channel.basic_publish(exchange=exchange_baby_monitor, routing_key=routing_key_smart_tv, body="ALERT! Emma isn't breathing")

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
    queue=queue_smartphone, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
