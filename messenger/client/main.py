"""
Функции ​к​лиента:​
- сформировать ​​presence-сообщение;
- отправить ​с​ообщение ​с​ерверу;
- получить ​​ответ ​с​ервера;
- разобрать ​с​ообщение ​с​ервера;
- параметры ​к​омандной ​с​троки ​с​крипта ​c​lient ​​<addr> ​[​<port>]:
- addr ​-​ ​i​p-адрес ​с​ервера;
- port ​-​ ​t​cp-порт ​​на ​с​ервере, ​​по ​у​молчанию ​​8000.
"""
import time
from random import randint
from argparse import ArgumentParser
from settings import DEFAULT_PORT, DEFAULT_IP
from socket import socket, AF_INET, SOCK_STREAM
from exceptions import CUSTOM_EXCEPTIONS, UsernameToLongError, \
    ResponseCodeLenError, MandatoryKeyError, ResponseCodeError
from jim.config import *
from jim.utils import send_message, get_message


class Client:
    def __init__(self, address, user_name):
        self._host = address
        self._username = self.validate_username(user_name)
        try:
            self._sock = socket(AF_INET, SOCK_STREAM)
            self._sock.connect(self._host)
        except ConnectionRefusedError:
            print('Сервер отклонил запрос на подключение.')
            exit(1)

        print(f'Клиент запущен (сервер: {address[0]}:{address[1]})')

    @staticmethod
    def validate_username(user_name):
        try:
            if user_name == 'Гость':
                user_name = input('Введите своё имя: ') or f'Гость_{randint(1,1000)}'
            if len(user_name) > 25:
                raise UsernameToLongError
        except UsernameToLongError as ce:
            print(ce)
            exit(1)
        return user_name

    @staticmethod
    def translate_response(response):
        if not isinstance(response, dict):
            raise TypeError
        if RESPONSE not in response:
            raise MandatoryKeyError(RESPONSE)
        code = response[RESPONSE]
        if len(str(code)) != 3:
            raise ResponseCodeLenError(code)
        if code not in RESPONSE_CODES:
            raise ResponseCodeError(code)
        return response

    def create_presence(self):
        message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self._username
            }
        }
        return message

    def main_loop(self):
        try:
            while True:
                request = self.create_presence()
                send_message(self._sock, request)
                response = get_message(self._sock)
                response = self.translate_response(response)
                print(response)
                return response
        except KeyboardInterrupt:
            print('Клиент закрыт по инициативе пользователя.')
        except ConnectionResetError:
            print('Соединение с сервером разорвано.')
        except CUSTOM_EXCEPTIONS as ce:
            print(ce)
        finally:
            self._sock.close()

    def close(self):
        self._sock.close()


def parse_args():
    parser = ArgumentParser(description='Запуск клиента.')
    parser.add_argument(
        'addr', nargs='?', default=f'{DEFAULT_IP}', type=str,
        help='IP адрес сервера'
    )
    parser.add_argument(
        'port', nargs='?', default=f'{DEFAULT_PORT}', type=int, help='порт сервера'
    )
    parser.add_argument(
        '-u',
        '--user',
        default='Гость',
        nargs='?',
        help='Имя пользователя(по умолчанию Гость_****)')
    result = parser.parse_args()
    if result.port not in range(1024, 65535):
        parser.error(
            f'argument port: invalid choice: {result.port} (choose from 1024-65535)'
        )
    return result


def run():
    args = parse_args()
    client = Client((args.addr, args.port), args.user)
    client.main_loop()


if __name__ == '__main__':
    run()
