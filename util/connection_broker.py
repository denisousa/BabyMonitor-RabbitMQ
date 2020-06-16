import pika


class Connection():
    def __init__(self):
        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()

    