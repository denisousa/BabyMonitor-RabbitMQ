from ...utils.config_broker import ConfigScenario
from publisher import SmartphonePublisher
from ...construct_scenario import (exchange_baby_monitor,
                                   queue_smartphone,
                                   routing_key_smartphone)


class SmartphoneSubscriber(ConfigScenario):
    def __init__(self):
        self.declare_exchange(exchange_baby_monitor, 'direct')
        self.declare_queue(queue_smartphone)
        self.bind_exchange_queue(exchange_baby_monitor,
                                 queue_smartphone,
                                 routing_key_smartphone)

    def consume_message(self):
        print(" [*] Smartphone waiting for messages. To exit press CTRL+C")
        count_time = 0

        def callback_smartphone(ch, method, properties, body):
            if body['type'] == 'notification':
                count_time += 1

                if count_time >= 5:
                    SmartphonePublisher().forward_message(body)

        self.channel.basic_consume(
            queue=queue_smartphone,
            on_message_callback=callback_smartphone,
            auto_ack=True,
        )

        self.channel.start_consuming()

        self.connection.close()
