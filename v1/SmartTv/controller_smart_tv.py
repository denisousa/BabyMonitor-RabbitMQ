#!/usr/bin/env python
import sys
sys.path.append("../")
from model_smart_tv import Smart_TV
import threading


class Smart_tv_controller:
    def __init__(self):
        self.smart_tv = Smart_TV()

    def turn_on(self):
        self.smart_tv.button_is_pressed = True
        self.smart_tv.start()

    def turn_off(self):
        self.smart_tv.button_is_pressed = False

    def start_app(self):
        self.smart_tv.application = True
        self.smart_tv.application_thread = threading.Thread(
            target=self.smart_tv.application_func, args=()
        )
        self.smart_tv.application_thread.start()

        if self.smart_tv.application_thread.isAlive():
            return 1
        return 0

    def stop_app(self):
        self.smart_tv.application = False
        self.smart_tv.status = True

    def get_status(self):
        return self.smart_tv.status

    def get_application(self):
        return self.smart_tv.application

    def get_message(self):
        return self.smart_tv.message

    def is_on(self):
        return self.smart_tv.isAlive()
