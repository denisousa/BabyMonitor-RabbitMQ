from util.config_broker import ConfigScenario
from model.publisher.smartphone_publisher import SmartphonePublisher
from util.construct_scenario import (exchange,
                                   queue_smartphone,
                                   routing_key_smartphone)
from model.buisness.smartphone_business import (wait_user_confirm,
                      check_is_notification,
                      check_user_confirm,
                      send_confirm_baby_monitor,
                      forward_message_smart_tv)
from threading import Thread


class SmartphoneSubscriber(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, 'direct')
        self.declare_queue(queue_smartphone)
        self.bind_exchange_queue(exchange,
                                 queue_smartphone,
                                 'bm_info')

    def run(self):
        pass

    def consume_message_baby_monitor(self):
        print(" [*] Smartphone waiting for messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_smartphone,
            on_message_callback=callback_smartphone,
            auto_ack=True,
        )

        self.channel.start_consuming()
        self.connection.close()

    def consume_message_tv(self):
        print(" [*] Smartphone waiting for messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_smartphone,
            on_message_callback=callback_smartphone,
            auto_ack=True,
        )

        self.channel.start_consuming()
        self.connection.close()

    def callback_smartphone(ch, method, properties, body):
        notification = check_is_notification(body)
        if notification:
            # TODO chamar o método de exibir a pseudo alerta
            confirm = wait_user_confirm()
            if confirm:
                send_confirm_baby_monitor(body)
            else:
                forward_message_smart_tv(body)
                # TODO como fazer para que o smartphone passe a consumir de outro tópico
                # Talvez outra classe que deva ser instanciada? by Denis