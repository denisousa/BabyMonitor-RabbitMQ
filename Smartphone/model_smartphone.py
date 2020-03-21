import pika
import random
import sys
import time
sys.path.append('../')
from construct_scenario import engine, meta, exchange_baby_monitor, queue_smart_tv, queue_smartphone, routing_key_smart_tv, routing_key_smartphone
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean
import sqlalchemy as db
import threading


class Smartphone(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.engine = engine
        self.meta = meta
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_bind(
                exchange=exchange_baby_monitor, queue=queue_smartphone, routing_key=routing_key_smartphone)

        self.channel.queue_bind(
                exchange=exchange_baby_monitor, queue=queue_smart_tv, routing_key=routing_key_smart_tv)
        
        self.is_producer = False
        self.is_consumer = False

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
        
        self.connection.close()

    def read_message(self, message):

        if 'NOTIFICATION' in message: 
            data = str(message).replace(('NOTIFICATION: ', ''))
            data = eval(data)
            
            if not data['breathing']: 
                print(f"Alert: Baby Emma hasn't been breathing for {data['time_no_breathing']} seconds!")
            
            elif not data['crying']:
                print('Alert: Baby Emma is crying.')
        
        else: 
            print("It's all ok. :)")    

    
    def confirm_notification(self):
        pass


    '''def create_table_smartphone(self):
        smartphone = Table(
        'smartphone', meta, 
        Column('id', Integer, primary_key = True, autoincrement=True), 
        Column('notification', String), 
        )
        meta.create_all(engine)
        
        return smartphone'''
    
    def get_data_baby_monitor(self):
        bm = db.Table('baby_monitor', self.meta, autoload=True, autoload_with=self.engine)
        conn = self.engine.connect()
        query = db.select([bm])
        result = conn.execute(query).fetchall()
        if result: 
            return result[-1]
        else: 
            return 0 