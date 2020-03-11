import pika
import random
import sys
import time
sys.path.append('../')
from construct_scenario import queue_smartphone, queue_smart_tv, routing_key_smart_tv, routing_key_smartphone, exchange_baby_monitor
from sqlalchemy import Table, Column, String, Integer

class Smartphone():

    def __init__(self, connection, channel):

        self.connection = connection
        self.channel = channel

    def start_connection(self):
        print(' [*] Smartphone waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
            self.read_message(body)

        self.channel.basic_consume(
            #autoack vai ser manual
            queue=queue_smartphone, on_message_callback=callback, auto_ack=False)

        '''channel.basic_consume(
            queue=queue_smart_tv, on_message_callback=callback, auto_ack=True)'''

        self.channel.start_consuming()

    def forward_to_tv(self, message):
        channel.basic_publish(exchange=exchange_baby_monitor, routing_key=routing_key_smart_tv, body="ALERT! Emma isn't breathing")

    def read_message(self, message):
        message = eval(message)
        if not message['breathing'] and message['time_no_breathing'] > 3:
            print("ALERT! Emma isn't breathing")
            delay = time.time()
            #ver uma forma de resgatar esse ack
            while not ack: 
                delay = time.time() - delay
            
                if delay >= 5: 
                    print('Forwarding to TV')
                    self.forward_to_tv(str(message))
                
                break

    def create_table_smartphone(engine, meta):
        smartphone = Table(
        'smartphone', meta, 
        Column('id', Integer, primary_key = True, autoincrement=True), 
        Column('notification', String), 
        )
        meta.create_all(engine)
        
        return smartphone

    def insert_smartphone(smartphone, engine):
        conn = engine.connect()
        new_data = smartphone.insert().values(notification="Sou uma notificacao")
        conn.execute(new_data)