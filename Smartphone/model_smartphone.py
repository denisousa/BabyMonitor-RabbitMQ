import sys
sys.path.append("../")
from construct_scenario import (engine,
                                meta,
                                exchange_baby_monitor,
                                queue_smartphone,
                                routing_key_smartphone,
                                routing_key_baby_monitor)
import pika
import threading


class SmartphoneConsumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.engine = engine
        self.meta = meta
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=exchange_baby_monitor, exchange_type="direct"
        )
        self.channel.queue_declare(queue_smartphone)
        self.channel.queue_bind(
            exchange=exchange_baby_monitor,
            queue=queue_smartphone,
            routing_key=routing_key_smartphone,
        )
        self.message = ""
        self.button_is_pressed = False
        self.is_notification = False

    def run(self):
        if self.button_is_pressed:
            print(" [*] Smartphone waiting for messages. To exit press CTRL+C")

            def callback_smartphone(ch, method, properties, body):
                if "NOTIFICATION" in str(body):
                    self.is_notification = True
                    self.message = str(body)
                else:
                    self.is_notification = False
                    self.message = str(body).replace('b"STATUS: ', "")
                    self.message = self.message.replace('"', "")

            self.channel.basic_consume(
                queue=queue_smartphone,
                on_message_callback=callback_smartphone,
                auto_ack=True,
            )

            self.channel.start_consuming()

            self.connection.close()


class SmartphoneProducer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=exchange_baby_monitor, exchange_type="direct"
        )
        self.button_is_pressed = False

    def run(self):
        message = "CONFIRMATION: Notification received!"
        self.channel.basic_publish(
            exchange=exchange_baby_monitor,
            routing_key=routing_key_baby_monitor,
            body=message,
        )
