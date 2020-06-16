from model.publisher.smartphone_publisher import SmartphonePublisher
from time import sleep


def check_is_notification(message):
    if message['type'] == 'notification':
        return True

def forward_message_smart_tv(message):
    SmartphonePublisher().forward_message(message)

def send_confirm_baby_monitor(message):
    SmartphonePublisher().publish_confirmation(message)

def check_user_confirm():
    # TODO pegar a confirmação do usuário
    pass

def wait_user_confirm():
    for i in range(5):
        sleep(1)
        confirm = check_user_confirm()
        if confirm:
            break

