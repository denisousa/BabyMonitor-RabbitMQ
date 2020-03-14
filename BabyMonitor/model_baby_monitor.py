import pika
from time import sleep
import sys
from generate_data import *
sys.path.append('../')
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean
from construct_scenario import main
import sqlalchemy as db
import threading
import sqlite3


class Baby_Monitor(threading.Thread):
    def __init__(self):
        self.engine = main[0]
        self.meta = main[1]
        self.channel = main[2]
        self.exchange_baby_monitor = main[7]
        self.routing_key_smartphone = main[6]
        
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.bm = self.create_table_baby_monitor()
        self.button_is_pressed = False

    def run(self):

        while self.button_is_pressed:
            data_from_baby(self)

            line = self.get_data_baby_monitor()

            keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')

            message = str(dict(zip(keys, line)))
            self.channel.basic_publish(exchange=self.exchange_baby_monitor, routing_key=self.routing_key_smartphone, body=message)

            print(" [x] Sent Topic: %r | Message: %r" % (self.routing_key_smartphone, message))
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
        conn = self.engine.connect()
        query = self.bm.insert()
        conn.execute(query, data)

    def get_data_baby_monitor(self):
        conn = self.engine.connect()
        query = db.select([self.bm])
        result = conn.execute(query).fetchall()
        if result: 
            return result[-1]
        else: 
            return 0 