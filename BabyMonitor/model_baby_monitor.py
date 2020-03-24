import pika
from time import sleep
import sys
from generate_data import *
sys.path.append('../')
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean, String
from construct_scenario import *
import sqlalchemy as db
import threading

semaphore = threading.Semaphore()
notif_confirm = [False, False]

class Baby_Monitor(threading.Thread):
    def __init__(self):
        self.engine = engine
        self.meta = meta
        self.channel = channel
        self.is_consumer = False
        self.is_producer = False
        
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.bm = self.create_table_baby_monitor()
        self.button_is_pressed = False

    def run(self):
        global semaphore, notif_confirm

        if self.is_consumer:  
            self.channel.queue_bind(
            exchange=exchange_baby_monitor, queue = queue_baby_monitor, routing_key=routing_key_baby_monitor)
        
            def callback(ch, method, properties, body):
                print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
                semaphore.acquire()
                notif_confirm[1] = True
                semaphore.release()

            self.channel.basic_consume(
                queue= queue_baby_monitor, on_message_callback=callback, auto_ack=True)

            self.channel.start_consuming()
        
        if self.is_producer:
            while self.button_is_pressed:
                if notif_confirm[0]:
                    if notif_confirm[1]:
                        data_from_baby(self, -1)
                        semaphore.acquire()
                        notif_confirm[0] = False
                        notif_confirm[1] = False
                        semaphore.release()
                    else: 
                        data_from_baby(self, 1)
                else: 
                    data_from_baby(self, 0)

                line = self.get_data_baby_monitor()
                keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')
                data = dict(zip(keys, line))
                message = str(data)
                if data['crying'] or data['time_no_breathing'] >= 5:
                    message = 'NOTIFICATION: ' + message
                    semaphore.acquire()
                    notif_confirm[0] = True
                    semaphore.release()

                else: 
                    message = 'STATUS: ' + message 

                self.channel.basic_publish(exchange=exchange_baby_monitor, routing_key=routing_key_smartphone, body=message)

                print(" [x] Sent Topic: %r | Message: %r" % (routing_key_smartphone, message))
                sleep(2)
        
        print('Closing connection...')
        self.connection.close()

    def create_table_baby_monitor(self):
        try:
            baby_monitor_table = Table(
                "baby_monitor",
                self.meta,
                Column("id", Integer, primary_key=True, autoincrement=True),
                Column("breathing", Boolean),
                Column("time_no_breathing", Integer),
                Column("crying", Boolean),
                Column("sleeping", Boolean),
            )
            self.meta.create_all(self.engine)

            return baby_monitor_table
        except:
            connection = self.engine.connect()
            bm = db.Table('baby_monitor', self.meta, autoload=True, autoload_with=self.engine)
            return bm

    def insert_baby_monitor(self, data):
        try:
            conn = self.engine.connect()
            query = self.bm.insert()
            conn.execute(query, data)
            print('Success')
        except:
            conn = self.engine.connect()
            conn.rollback()
            print('Failed')

    def get_data_baby_monitor(self):
        conn = self.engine.connect()
        query = db.select([self.bm])
        result = conn.execute(query).fetchall()

        if result: 
            return result[-1]
        else: 
            return 0 