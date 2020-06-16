from util.config_broker import ConfigScenario
from util.construct_scenario import (exchange,
                                   queue_baby_monitor,
                                   queue_smartphone,
                                   queue_smart_tv,
                                   routing_key_baby_monitor)
from model.buisness.baby_monitor_business import check_confirm_notification
from threading import Thread


class BabyMonitorSubscriber(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, 'direct')
        self.declare_queue(queue_baby_monitor)
        self.declare_queue(queue_smartphone)
        self.declare_queue(queue_smart_tv)
        self.bind_exchange_queue(exchange,
                                 queue_baby_monitor,
                                 routing_key_baby_monitor)

    def run(self):
        self.check_baby_status()

    def check_baby_status(self):
        print(" [*] BabyMonitor waiting for Smartphone messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_baby_monitor,
            on_message_callback=self.callback_baby_monitor,
            auto_ack=True,
        )

        self.channel.start_consuming()
        self.connection.close()

    def callback_baby_monitor(ch, method, properties, body):
        confirm = check_confirm_notification()
        if confirm:
            # TODO forçar geração status do bebe ser normal
            pass

