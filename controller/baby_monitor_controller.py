from model.publisher.baby_monitor_publisher import BabyMonitorPublisher
from model.subscriber.baby_monitor_subscriber import BabyMonitorSubscriber


class BabyMonitorController():
    # subscriber = BabyMonitorSubscriber()
    # subscriber.start()
    # subscriber.join()

    publisher = BabyMonitorPublisher()
    publisher.start()
    publisher.join()

