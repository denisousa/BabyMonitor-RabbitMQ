import json


def construct_message(topic: str = '', type_msg: str = '', data: dict = {}) -> dict:
    return json.dumps({
        'topic': topic,
        'type_msg': type_msg,
        'data': data
    })