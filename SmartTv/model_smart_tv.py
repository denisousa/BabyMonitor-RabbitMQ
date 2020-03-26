import pika
import sys
import random
sys.path.append('../')
from construct_scenario import *
from sqlalchemy import Table, Column, String, Integer
import threading

class SmartTV():

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type="topic")
        self.channel.queue_declare(queue_smart_tv)
        self.channel.queue_bind(
            exchange=exchange_baby_monitor, queue=queue_smart_tv, routing_key=routing_key_smart_tv)

        self.status = True
        self.application = False
        self.application_thread = threading.Thread(target=self.aplication_func, args=())
        self.button_is_pressed = False
        self.message_received = ''

    def start_connection(self):
        if self.button_is_pressed:
            if self.status:
                print('TV is unlocked.')
            
                print(' [*] Smart Tv waiting for messages. To exit press CTRL+C')

                def callback_smart_tv(ch, method, properties, body):

                    print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
                    self.message_received = str(body).replace('b', '')
                
                self.channel.basic_consume(
                    queue=queue_smart_tv, on_message_callback=callback_smart_tv, auto_ack=True)

                self.channel.start_consuming()
            else:
                print("TV is locked. Can't receive messages.")

    def aplication_func(self):
        while self.application:
            self.status = False
        self.start_connection()
