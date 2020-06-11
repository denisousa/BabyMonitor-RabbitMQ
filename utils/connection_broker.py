import pika


class Connection():
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()


class ConfigScenario(Connection):
    def declare_exchange(self, exchange, exchange_type):
        self.channel.exchange_declare(
            exchange=exchange, exchange_type=exchange_type
        )
    
    def declare_queue(self, queue):
        self.channel.queue_declare(queue)

    def bind_exchange_queue(self, exchange, queue, routing_key):
        self.channel.queue_bind(
            exchange=exchange_baby_monitor,
            queue=queue_smartphone,
            routing_key=routing_key_smartphone,
        )

    