from util.construct_scenario import (exchange,
                                routing_key_smartphone,
                                routing_key_smart_tv,
                                routing_key_baby_monitor)
from util.config_broker import ConfigScenario
from util.body_message import construct_message
from threading import Thread


class SmartphonePublisher(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, 'direct')

    def run(self):
        pass

    def publish_status(self):
        info = {'msg': 'Normal operation'}
        message = construct_message('sm_info',
                                    'info',
                                    info)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key_smartphone,
            body=message,
        )

    def publish_confirmation(self):
        confirmation = {'msg': 'Notification received!'}
        message = construct_message('bm_msg',
                                    'confirmation',
                                    confirmation)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key_baby_monitor,
            body=message,
        )

    def forward_message(self):
        notification = {'msg': 'Notification sent!'}
        message = construct_message('st_msg',
                                    'notification',
                                    notification)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key_smart_tv,
            body=message,
        )
