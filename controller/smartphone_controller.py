from model.publisher.smartphone_publisher import SmartphonePublisher
from model.subscriber.smartphone_subscriber import SmartphoneSubscriber


class SmartphoneController():
    # subscriber = SmartphonePublisher()
    # subscriber.start()
    # subscriber.join()

    publisher = SmartphoneSubscriber()
    publisher.start()
    publisher.join()