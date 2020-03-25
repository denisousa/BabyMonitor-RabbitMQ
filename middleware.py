import pika
import sys
sys.path.append('./BabyMonitor')
sys.path.append('./Smartphone')
sys.path.append('./SmartTv')
from construct_scenario import *
from SmartTv.controller_smart_tv import *
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

    def get_queues_and_exchanges_and_routings(self):
        client = Client('localhost:15672', 'guest', 'guest')
        queues = [q['name'] for q in client.get_queues()]
        exchanges = [e['name'] for e in client.get_exchanges()]
        routing_keys = [r['routing_key'] for r in client.get_bindings()]

        # Exclude first 6 exchanges default rabbitmq
        return [queues, exchanges[7:], routing_keys]

    def subscribe_in_all_queues(self):
        queues = self.get_queues_and_exchanges_and_routings()[0]
        exchanges = self.get_queues_and_exchanges_and_routings()[1]
        routings = self.get_queues_and_exchanges_and_routings()[2]

        exchange_conn_queue = []
        for exchange in exchanges:
            for queue in queues:
                try:
                    self.channel.queue_bind(
                        exchange=exchange, queue=queue, routing_key='*')
                    exchange_conn_queue.append((exchange, queue))
                except:
                    continue
        
        return queues, exchanges, routings
        
    def run(self):
        
        queues, exchanges, routings = self.subscribe_in_all_queues()

        def callback(ch, method, properties, body):
            print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
            if 'tv' in str(method.routing_key):
                self.time_no_response = 0
                
            self.read_message(str(body), routings, exchanges)
        
        for q in queues:
            self.channel.basic_consume(
                queue=q, on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()
    
    def read_message(self, message, routings, exchanges):
        global watch_time, semaphore 

        if 'NOTIFICATION' in message:
            data = message.replace('b"NOTIFICATION: ', '')
            data = data.replace('"', '')
            data = eval(data)
            message = 'NOTIFICATION: ' + str(data)
            watch_time = threading.Thread(target=watch_confirmation, args=(self, message, routings, exchanges, ))
            watch_time.start()

        if 'CONFIRMATION' in message:
            semaphore.acquire()
            self.time_no_response = 0
            semaphore.release()

    def publish_message(self, message, routings, exchanges):
        routing_key = [routing for routing in routings if 'tv_route' in routing][0]
        for exchange in exchanges:
            try:
                print('Trying to send message to tv')
                self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
                break
            except:
                pass

    def forward_message(self, message, routings, exchanges):
        if get_status():
            self.publish_message(message, routings, exchanges)
        else:
            stop_app()
            self.publish_message(message, routings, exchanges)
            start_app()

def watch_confirmation(middleware, message, routings, exchanges):
    global semaphore

    semaphore.acquire()
    middleware.time_no_response = 1
    semaphore.release()

    while middleware.time_no_response != 0: 
        semaphore.acquire()
        middleware.time_no_response = int(time.time() - middleware.time_no_response)
        semaphore.release()
        print('Time no response: ', middleware.time_no_response)

        if middleware.time_no_response > 5: 
            print('Message will be forwarded to Smart TV')
            middleware.forward_message(message, routings, exchanges)
            middleware.time_no_response = 0

def main():
    thread_middleware = Middleware()
    thread_middleware.start()
    

if __name__ == '__main__':
    main()