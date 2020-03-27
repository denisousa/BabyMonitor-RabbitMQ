import pika
import sys
import random
sys.path.append('../')
from construct_scenario import *
import threading

class Smart_TV(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type="direct")
        self.queue = self.channel.queue_declare(queue_smart_tv, arguments={'x-max-priority': 10})
        self.channel.queue_bind(
            exchange=exchange_baby_monitor, queue=queue_smart_tv, routing_key=routing_key_smart_tv)

        self.status = True
        self.application = False
        self.application_thread = None
        self.button_is_pressed = False
        self.message = ''

    def run(self):
        while self.button_is_pressed:
            print(' [*] Smart Tv waiting for messages. To exit press CTRL+C')

            if self.status:
                print('TV is unlocked.')

            else:
                print('TV is locked')

            def callback_smart_tv(ch, method, properties, body):
                print(" [SmartTv] Receive Topic: %r | Message: %r" % (method.routing_key, body))
                self.message = str(body).replace('b"', '')
                self.message = self.message.replace('"', '')
            
            if self.status:
                self.channel.basic_consume(
                    queue=queue_smart_tv, on_message_callback=callback_smart_tv, auto_ack=True)

                if self.queue.method.message_count == 0:
                    self.message = ''

                self.channel.start_consuming()
        self.connection.close()

    def aplication_func(self):
        while self.application:
            self.status = False
