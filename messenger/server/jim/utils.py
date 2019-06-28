import json
from settings import ENCODING, MAX_PACKAGE_LENGTH


def dict_to_bytes(dict_msg):
    if isinstance(dict_msg, dict):
        json_msg = json.dumps(dict_msg)
        bytes_msg = json_msg.encode(ENCODING)
        return bytes_msg
    else:
        raise TypeError


def bytes_to_dict(bytes_msg):
    if isinstance(bytes_msg, bytes):
        json_msg = bytes_msg.decode(ENCODING)
        try:
            message = json.loads(json_msg)
        except json.decoder.JSONDecodeError:
            raise ConnectionResetError
        if isinstance(message, dict):
            return message
        else:
            raise TypeError
    else:
        raise TypeError


def send_message(sock, message):
    bytes_presence = dict_to_bytes(message)
    sock.send(bytes_presence)


def get_message(sock):
    bytes_response = sock.recv(MAX_PACKAGE_LENGTH)
    response = bytes_to_dict(bytes_response)
    return response
