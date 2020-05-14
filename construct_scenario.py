import pika
from sqlalchemy import create_engine, MetaData


engine = create_engine("sqlite:///../app.db")
meta = MetaData()

routing_key_baby_monitor = "baby_monitor_route"
routing_key_smart_tv = "smart_tv_route"
routing_key_smartphone = "smartphone_route"
queue_baby_monitor = "queue_baby_monitor"
queue_smart_tv = "queue_smart_tv"
queue_smartphone = "queue_smartphone"
exchange_baby_monitor = "exchange_baby_monitor"



'''def declare_exchanges_queues():
    queue_baby_monitor = "queue_baby_monitor"
    queue_smart_tv = "queue_smart_tv"
    queue_smartphone = "queue_smartphone"
    exchange_baby_monitor = "exchange_baby_monitor"
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type="topic")
    channel.queue_declare(queue_baby_monitor)
    channel.queue_declare(queue_smartphone)
    channel.queue_declare(queue_smart_tv)
    connection.close()'''
