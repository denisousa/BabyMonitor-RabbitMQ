#!/usr/bin/env python
from model_baby_monitor import (BabyMonitorConsumer,
                                BabyMonitorProducer,
                                notif_confirm)


class Baby_monitor_controller:
    def __init__(self):

        self.monitor_producer = BabyMonitorProducer()
        self.monitor_consumer = BabyMonitorConsumer()

    # start conection
    def start(self):

        self.monitor_producer = BabyMonitorProducer()
        self.monitor_consumer = BabyMonitorConsumer()

        self.monitor_producer.button_is_pressed = True
        self.monitor_consumer.button_is_pressed = True

        self.monitor_consumer.start()
        self.monitor_producer.start()

    # stop conection
    def stop(self):

        self.monitor_producer.button_is_pressed = False
        self.monitor_consumer.button_is_pressed = False

    # get data from db
    def get_data(self):

        return self.monitor_producer.message

    # check if a confirmation has been sent
    def get_confirmation(self):
        if notif_confirm[0]:
            if notif_confirm[1]:
                return "Confirmation received."
            else:
                return "Pending notification."
        else:
            return ""

    # get info about baby
    def get_status(self):
        return self.monitor_producer.get_data_baby_monitor()
