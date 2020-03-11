#!/usr/bin/env python
import pika
import sys
sys.path.append('../')
from construct_scenario import queue_smartphone, queue_smart_tv, routing_key_smart_tv, routing_key_smartphone, exchange_baby_monitor
import model_smartphone

def turn_on():

    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_bind(
            exchange='exchange_baby_monitor', queue=queue_smartphone, routing_key=routing_key_smartphone)

    channel.queue_bind(
            exchange='exchange_baby_monitor', queue=queue_smart_tv, routing_key=routing_key_smart_tv)

    smartphone = Smartphone(connection, channel)
    smartphone.start_connection()

def confirm_notification():
    '''minha ideia é controlar o envio do ack aqui. 
    O ack só é enviado quando clica pra confirmar'''
    pass