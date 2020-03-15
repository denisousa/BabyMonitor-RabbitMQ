import pika
import random
import sys
import time
sys.path.append('../')
from construct_scenario import main
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean
import sqlalchemy as db
import threading

class Smartphone(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.engine = main[0]
        self.meta = main[1]
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()

        self.channel.queue_bind(
                exchange=main[7], queue=queue_smartphone, routing_key=routing_key_smartphone)

        self.channel.queue_bind(
                exchange=main[7], queue=queue_smart_tv, routing_key=routing_key_smart_tv)

        #self.smp = self.create_table_smartphone()
        self.button_is_pressed = False

    def run(self):
        while self.button_is_pressed:
            print(' [*] Smartphone waiting for messages. To exit press CTRL+C')

            def callback(ch, method, properties, body):
                print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
                self.read_message(body)

            self.channel.basic_consume(
        
                queue=queue_smartphone, on_message_callback=callback, auto_ack=False)

            self.channel.start_consuming()
        
        connection.close()

    '''def forward_to_tv(self, message):
        channel.basic_publish(exchange=exchange_baby_monitor, routing_key=routing_key_smart_tv, body="ALERT! Emma isn't breathing")'''

    def read_message(self, message):
        message = eval(message)
        if not message['breathing'] and message['time_no_breathing'] > 3:
            print("ALERT! Emma isn't breathing")    

    '''def create_table_smartphone(self):
        smartphone = Table(
        'smartphone', meta, 
        Column('id', Integer, primary_key = True, autoincrement=True), 
        Column('notification', String), 
        )
        meta.create_all(engine)
        
        return smartphone'''
    
    def get_data_baby_monitor(self):
        conn = engine.connect()
        bm = db.Table('baby_monitor', meta, autoload=True, autoload_with=engine)
        query = db.select([bm])
        result = conn.execute(query).fetchall()
        if result: 
            return result[-1]
        else: 
            return 0 