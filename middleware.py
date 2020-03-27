import pika
import sys
sys.path.append('./BabyMonitor')
sys.path.append('./Smartphone')
sys.path.append('./SmartTv')
from construct_scenario import *
from SmartTv.controller_smart_tv import *
from Smartphone.controller_smartphone import smartphone_confirm_notification
import threading
from pyrabbit.api import Client
import time
import itertools

semaphore = threading.BoundedSemaphore()
init = 0

class Middleware(threading.Thread):
    def __init__(self, is_adapted):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.queue = 'middleware'
        self.channel.queue_declare(self.queue)
        self.time_no_response = 0
        self.count = 0
        self.is_adapted = is_adapted

    def get_bindings(self):
        client = Client('localhost:15672', 'guest', 'guest')
        bindings = client.get_bindings()
        bindings = bindings[4:]

        return bindings

    def subscribe_in_all_queues(self):
        
        bindings = self.get_bindings()
        for i in range(len(bindings)):
            if not 'baby_monitor' in bindings[i]['routing_key']:
                self.channel.queue_bind(
                    exchange=bindings[i]['source'], queue=self.queue, routing_key=bindings[i]['routing_key'])

        return bindings
        
    def run(self):
        
        bindings = self.subscribe_in_all_queues()
        time.sleep(2)
        def callback(ch, method, properties, body):
            print("[MIDDLEWARE] Receive Topic: %r | Message: %r" % (method.routing_key, body))
            if 'tv' in str(method.routing_key):
                self.time_no_response = 0
                print('### TV successfully received the message.')
            
            else:
                self.read_message(str(body), bindings)
        
        for i in range(len(bindings)):
            if not 'baby_monitor' in bindings[i]['destination']:
                self.channel.basic_consume(
                    queue=bindings[i]['destination'], on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()
    
    def read_message(self, message, bindings):
        global semaphore, init
        if 'NOTIFICATION' in message:

            self.count += 1
            
            if self.count == 1:
                init = time.time()

            else:
                self.time_no_response = time.time() - init
                print(f'* Time No response: {int(self.time_no_response)} seconds.')
                if self.time_no_response >= 5:
                    self.forward_message(message, bindings)

        if 'STATUS' in message:
            self.count = 0 
            self.time_no_response = 0 

    def forward_message(self, message, bindings):
        if smart_tv_get_status():
            self.publish_message(message, bindings)
        else:
            if self.is_adapted:
                print('\n### Executing adaptation...')
                print('\tStopping application')
                smart_tv_stop_app()
                self.publish_message(message, bindings)
                time.sleep(2)
                print('\tReopening application\n')
                smart_tv_start_app()
            else:
                print('### Unable to forward to TV...')

    def publish_message(self, message, bindings):
        ex_rt = []

        for i in range(len(bindings)):
            if 'monitor' not in bindings[i]['destination'] and 'smartphone' not in bindings[i]['destination']:
                ex_rt = [(bindings[i]['source'], bindings[i]['routing_key'])]

        for i in ex_rt:
            try:
                print('\n### Trying to send message to tv...')
                self.channel.basic_publish(exchange=i[0], routing_key=i[1], body=message)
                self.count = 0
                smartphone_confirm_notification()
                print('### Sending confirmation to monitor...\n')
                break
            except:
                pass

def main(is_adapted):
    thread_middleware = Middleware(is_adapted)
    thread_middleware.start()