import pika
import sys
sys.path.append('./BabyMonitor')
sys.path.append('./Smartphone')
sys.path.append('./SmartTv')
from construct_scenario import *
from SmartTv.controller_smart_tv import *
from Smartphone.controller_smartphone import *
from BabyMonitor.controller_baby_monitor import *
import threading
from pyrabbit.api import Client
import time

# Se insrever em todos os tópicos - OK
# Receber todas as mensagens dos tópicos - OK
# Mensagem tipo notificação, começa a contar tempo
# Quando tempo alcança x, ele tenta enviar a msg que recebeu pra tv (get_Status)
# Se TV bloqueada, stop application, envia notificação e start application.

watch_time = None
semaphore = threading.BoundedSemaphore()

class Middleware(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.time_no_response = 0

    def get_queues_and_exchanges(self):
        client = Client('localhost:15672', 'guest', 'guest')
        queues = [q['name'] for q in client.get_queues()]
        exchanges = [q['name'] for q in client.get_exchanges()]

        # Exclude first 6 exchanges default rabbitmq
        return [queues, exchanges[7:]]

    def subscribe_in_all_queues(self):
        queues = self.get_queues_and_exchanges()[0]
        exchanges = self.get_queues_and_exchanges()[1]

        exchange_conn_queue = []
        for exchange in exchanges:
            for queue in queues:
                try:
                    self.channel.queue_bind(
                        exchange=exchange, queue=queue, routing_key='*')
                    exchange_conn_queue.append((exchange, queue))
                except:
                    continue
        
        return exchange_conn_queue
        
    def run(self):
        
        def callback(ch, method, properties, body):
            print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
            self.read_message(str(body))
        
        exchange_conn_queue = self.subscribe_in_all_queues()
        
        for q in exchange_conn_queue:
            self.channel.basic_consume(
                queue=q[1], on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()
    
    def read_message(self, message):
        global watch_time, semaphore 

        if 'NOTIFICATION' in message:
            watch_time = threading.Thread(target=watch_confirmation, args=(self, ))
            watch_time.start()

        if 'CONFIRMATION' in message:
            semaphore.acquire()
            self.time_no_response = 0
            semaphore.release()

    def forward_message(self):
        pass

def watch_confirmation(middleware):
    global semaphore

    semaphore.acquire()
    middleware.time_no_response = int(time.time())
    semaphore.release()

    while middleware.time_no_response != 0: 
        semaphore.acquire()
        middleware.time_no_response = int(time.time() - middleware.time_no_response)
        semaphore.release()

        if middleware.time_no_response > 5: 
            middleware.forward_message()

def main():
    thread_middleware = Middleware()
    thread_middleware.start()
    

if __name__ == '__main__':
    main()