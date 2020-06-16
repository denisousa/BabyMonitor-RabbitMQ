def check_confirm_notification():
    pass


def generate_notification(status):
    if status:
        return {'msg': 'Alert! The child is not breathing'}
    else:
        return {'msg': 'Alert! The child is crying'}