import pika
import sys
import random
sys.path.append('../')
from construct_scenario import queue_smart_tv, routing_key_smart_tv, exchange_baby_monitor
from sqlalchemy import Table, Column, String, Integer

class Smart_TV():

    def __init__(self, connection, channel):
        
        self.connection = connection
        self.channel = channel

        self.status = True
        self.application = False    

    def start_connection(self):
        
        print(' [*] Smart Tv waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            if self.status:
                print(" [x] Receive Topic: %r | Message: %r" % (method.routing_key, body))
            else:
                self.channel.basic_publish(exchange=exchange_baby_monitor, routing_key=routing_key_smart_tv, body="Unable to show notification.")

        self.channel.basic_consume(
            queue=queue_smart_tv, on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()


    def create_table_smart_tv(engine, meta):
        smart_tv_table = Table(
            "smart_tv",
            meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("command", String),
        )
        meta.create_all(engine)

        return smart_tv_table


    def insert_smart_tv(smart_tv, engine):
        conn = engine.connect()
        new_data = smart_tv.insert().values(command="Receive command from Smartphone")
        conn.execute(new_data)
