from util.config_broker import ConfigScenario
from util.construct_scenario import (exchange,
                                   queue_smart_tv,
                                   routing_key_smart_tv)
from threading import Thread


class SmartTvSubscriber(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, 'direct')
        self.declare_queue(queue_smart_tv)
        self.bind_exchange_queue(exchange,
                                 queue_smart_tv,
                                 'smart_tv_msg')

    def run(self):
        pass

    def consume_message(self):
        print(" [*] Tv waiting for messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_smart_tv,
            on_message_callback=callback_smartphone,
            auto_ack=True,
        )

        self.channel.start_consuming()
        self.connection.close()

    def callback_smartphone(ch, method, properties, body):
        available = check_available_tv()
        if available:
            show_alert()
            # TODO Envia mensagem no tópico smart_tv_msg
            # informando alerta exibido. Não entendi by Denis
        else:
            # TODO Envia mensagem no tópico smart_tv_msg
            # informando que está bloqueada. Não entendi by Denis
            pass

        