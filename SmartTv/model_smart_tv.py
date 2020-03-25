import pika
import sys
import random
sys.path.append('../')
from construct_scenario import *
from sqlalchemy import Table, Column, String, Integer
import threading


class Smart_TV(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        declare_exchanges_queues()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            exchange=exchange_baby_monitor, queue=queue_smart_tv, routing_key=routing_key_smart_tv)

        self.status = True
        self.application = False
        self.application_thread = threading.Thread(target=self.aplication_func, args=())
        self.button_is_pressed = False

    def run(self):
        while self.button_is_pressed:
            print(' [*] Smart Tv waiting for messages. To exit press CTRL+C')

            if self.status:
                print('TV is unlocked.')

            else:
                print('TV is locked')

            def callback_smart_tv(ch, method, properties, body):
                if self.status:
                    if 'tv' in method.routing_key:
                        print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
            
            self.channel.basic_consume(
                queue=queue_smart_tv, on_message_callback=callback_smart_tv, auto_ack=True)

            self.channel.start_consuming()

    def aplication_func(self):
        while self.application:
            self.status = False
