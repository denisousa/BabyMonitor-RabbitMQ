#!/usr/bin/env python
import pika
import sys

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

queue_smart_tv = 'queue_smart_tv'
routing_key = 'smart_tv_data'
exchange_smart_tv = 'exchange_smart_tv'

#Declare exchange of the type 'topic' with name 'exchange_smart_tv'
channel.exchange_declare(exchange=exchange_smart_tv, exchange_type='topic')
channel.queue_declare(queue_smart_tv, exclusive=True)

channel.queue_bind(
        exchange=exchange_smart_tv, queue=queue_smart_tv, routing_key=routing_key)


status = False

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))

channel.basic_consume(
    queue=queue_smart_tv, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
