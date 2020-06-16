from util.construct_scenario import (exchange,
                                routing_key_smart_tv)
from util.config_broker import ConfigScenario
from util.body_message import construct_message
from threading import Thread


class SmartTvPublisher(ConfigScenario, Thread):
    def __init__(self):
        ConfigScenario.__init__(self)
        Thread.__init__(self)
        self.declare_exchange(exchange, 'direct')

    def run(self):
        pass

    def publish_status(self):
        info = {'msg': 'Normal operation'}
        message = construct_message('st_info',
                                    'info',
                                    info)

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key_smart_tv,
            body=message,
        )
