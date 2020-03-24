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

# Se insrever em todos os tópicos
# Receber todas as mensagens do tópico
# Mensagem tipo notificação, começa a contar tempo
# Quando tempo alcança x, ele tenta enviar a msg que recebeu pra tv (get_Status)
# Se TV bloqueada, stop application, envia notificação e start application.

class Middleware(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_bind(
                exchange=exchange_baby_monitor, queue=queue_smartphone, routing_key=routing_key_smartphone)

        self.time_no_response = 0


    def run(self):
        while True:
            def callback(ch, method, properties, body):
                print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
            
            self.channel.basic_consume(
                queue=queue_smart_tv, on_message_callback=callback, auto_ack=True)

            self.channel.start_consuming()
    
    
    def get_notification(self, message):
        pass

    def get_confirmation(self):
        pass

    def watch_confirmation(self):
        pass

    def forward_message(self):
        pass

    