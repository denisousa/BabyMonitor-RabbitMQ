import pika
from sqlalchemy import create_engine, MetaData
from BabyMonitor.model_baby_monitor import create_table_baby_monitor, insert_baby_monitor
from Smartphone.model_smartphone import create_table_smartphone, insert_smartphone
from SmartTv.model_smart_tv import create_table_smart_tv, insert_smart_tv


engine = create_engine('sqlite:///app.db')
meta = MetaData()

bm = create_table_baby_monitor(engine, meta)
smt = create_table_smartphone(engine, meta)
tv = create_table_smart_tv(engine, meta)

queue_smartv = 'queue_smartv'
queue_smartphone = 'queue_smartphone'
routing_key_smart_tv= 'smart_tv_data'
routing_key_smartphone = 'smartphone_data'
exchange_baby_monitor = 'exchange_baby_monitor'

#Connection with RabbitMQ (Broker)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare exchange of the type 'topic' with name 'exchange_baby_monitor'
channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type='topic')
channel.queue_declare(queue_smartphone)
channel.queue_declare(queue_smartv)
