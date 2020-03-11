#!/usr/bin/env python
import pika
from time import sleep
import sys
from generate_data import data_from_baby
sys.path.append('../')
from construct_scenario import bm, engine, routing_key_smartphone
import model_baby_monitor

#código feito só pra teste, Denis livre pra adaptar a interface
    
def start():

    #Connection with RabbitMQ (Broker)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    monitor = Baby_Monitor(connection, channel)
    monitor.start_connection()        

def stop():
    pass