from util.construct_scenario import (
    exchange,
    routing_key_smartphone,
    routing_key_baby_monitor
)
from util.config_broker import ConfigScenario
from util.body_message import construct_message
from threading import Thread


class BabyMonitorPublisher(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, 'direct')

    def run(self):
        self.publish_status()

    def publish_status(self):
        info = {'msg': 'Normal operation'}
        message = construct_message('bm_info',
                                    'info',
                                    info)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key_baby_monitor,
            body=message,
        )

    def publish_info_baby(self):
        # TODO utilizar generate_data by Denis
        status = {
            "breathing": True,
            "time_no_breathing": 0,
            "crying": False,
        }
        message = construct_message('bm_msg',
                                    'status',
                                    status)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key_smartphone,
            body=message,
        )

    def send_notification(self, status):
        notification = generate_notification(status)
        message = construct_message('bm_msg',
                                    'notification',
                                    notification)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key_smartphone,
            body=message,
        )
