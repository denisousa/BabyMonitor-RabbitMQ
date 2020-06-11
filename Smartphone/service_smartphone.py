from model_smartphone import SmartphoneConsumer, SmartphoneProducer


class SmartphoneService:
    def __init__(self):
        self.smartphone_consumer = SmartphoneConsumer()

    def start(self):
        self.smartphone_consumer
        self.smartphone_consumer.button_is_pressed = True
        self.smartphone_consumer.start()

    def stop(self):
        self.smartphone_consumer
        self.smartphone_consumer.button_is_pressed = False

    def confirm_notification(self):
        self.smartphone_consumer
        self.smartphone_producer = None

        self.smartphone_consumer.is_notification = False
        self.smartphone_producer = SmartphoneProducer()
        self.smartphone_producer.start()
        self.smartphone_producer.join()

    def get_notification(self):
        self.smartphone_consumer
        return self.smartphone_consumer.is_notification

    def get_message(self):
        self.smartphone_consumer

        message = self.smartphone_consumer.message
        if "{" in message:
            return eval(message)

        message = message.replace("b'", "")
        message = message.replace('"', "")

        return message
