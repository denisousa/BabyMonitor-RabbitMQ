import sys
sys.path.append("../../utils")
from config_broker import ConfigScenario
sys.path.append("../..")
from construct_scenario import (exchange_baby_monitor,
                                routing_key_smart_tv,
                                routing_key_baby_monitor)


class SmartphonePublisher(ConfigScenario):
    def __init__(self):
        super().__init__()
        self.declare_exchange(exchange_baby_monitor, 'direct')


    def publish_confirmation(self):
        message = {'to_topic': 'bm_msg',
                   'type': 'confirmation',
                   'message': 'Notification received!'}

        self.channel.basic_publish(
            exchange=exchange_baby_monitor,
            routing_key=routing_key_baby_monitor,
            body=message,
        )

    def forward_message(self, message):
        self.channel.basic_publish(
            exchange=exchange_baby_monitor,
            routing_key=routing_key_smart_tv,
            body=message,
        )
