import pika
from time import sleep
import sys
from generate_data import data_from_baby
sys.path.append('../')
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean
from construct_scenario import bm, engine, routing_key_smartphone
import sqlalchemy as db


class Baby_Monitor():
    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel

    def start_connection():
        while True:
            data_from_baby()

            line = get_data_baby_monitor(bm, engine)

            keys = ('id', 'breathing', 'time_no_breathing', 'crying', 'sleeping')

            message = str(dict(zip(keys, line)))
            channel.basic_publish(exchange='exchange_baby_monitor', routing_key=routing_key_smartphone, body=message)

            print(" [x] Sent Topic: %r | Message: %r" % (routing_key_smartphone, message))
            sleep(2)

    def create_table_baby_monitor(engine, meta):
        baby_monitor_table = Table(
            "baby_monitor",
            meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("breathing", Boolean),
            Column("time_no_breathing", Integer),
            Column("crying", Boolean),
            Column("sleeping", Boolean),
        )
        meta.create_all(engine)

        return baby_monitor_table


    def insert_baby_monitor(bm, engine, data):
        conn = engine.connect()
        query = bm.insert()
        conn.execute(query, data)

    def get_data_baby_monitor(bm, engine):
        conn = engine.connect()
        query = db.select([bm])
        result = conn.execute(query).fetchall()
        if result: 
            return result[-1]
        else: 
            return 0 