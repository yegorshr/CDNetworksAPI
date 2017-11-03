import json


def encode_response(expected_data):
    return json.dumps(expected_data).encode('utf-8')
