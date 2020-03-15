#!/usr/bin/env python
import pika
import sys
import random
sys.path.append('../')
from construct_scenario import queue_smart_tv, routing_key_smart_tv, exchange_baby_monitor
import model_smart_tv


def turn_on():
    #Connection with RabbitMQ (Broker)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_bind(
            exchange=exchange_baby_monitor, queue=queue_smart_tv, routing_key=routing_key_smart_tv)
    
    tv = Smart_TV(connection, channel)
    tv.start_connection()

#ver uma forma de setar essas coisas
def start_app():
    application = True
    status = False