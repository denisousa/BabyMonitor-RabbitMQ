import pika
from sqlalchemy import create_engine, MetaData


engine = create_engine("sqlite:///../app.db")
meta = MetaData()

queue_baby_monitor = "queue_baby_monitor"
queue_smart_tv = "queue_smart_tv"
queue_smartphone = "queue_smartphone"
routing_key_baby_monitor = "confirmation_data"
routing_key_smart_tv = "smart_tv_data"
routing_key_smartphone = "babymonitor_data"
exchange_baby_monitor = "exchange_baby_monitor"

# Connectionhttps://hangouts.google.com/call/wuZMy8Wg_Kg4WkAbmL2IAEEE with RabbitMQ (Broker)
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# Declare exchange of the type 'topic' with name 'exchange_baby_monitor'
channel.exchange_declare(exchange=exchange_baby_monitor, exchange_type="topic")
channel.queue_declare(queue_baby_monitor)
channel.queue_declare(queue_smartphone)
channel.queue_declare(queue_smart_tv)
