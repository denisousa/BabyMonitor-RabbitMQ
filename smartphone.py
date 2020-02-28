#!/usr/bin/env python
import pika
import sys

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue_baby_monitor = 'queue_baby_monitor'
queue_smartphone = 'queue_smartphone'
routing_key_one = 'baby_monitor_data'
routing_key_second = 'smartphone_data'
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


def callback(ch, method, properties, body):
    print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))


channel.basic_consume(
    queue=queue_baby_monitor, on_message_callback=callback, auto_ack=True)

channel.basic_consume(
    queue=queue_smartphone, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
