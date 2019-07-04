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
from log.config import client_logger


class Client:
    def __init__(self, address, user_name):
        self.__logger = client_logger
        self._host = address
        self._sock = socket(AF_INET, SOCK_STREAM)
        try:
            self._username = self.validate_username(user_name)
            self._sock.connect(self._host)
        except (ConnectionRefusedError, OSError):
            info_msg = 'Сервер отклонил запрос на подключение.'
            self.__logger.warning(info_msg)
            print(info_msg)
            self.close()
            exit(1)
        info_msg = f'Клиент запущен (сервер: {address[0]}:{address[1]})'
        self.__logger.info(info_msg)
        print(info_msg)

    def validate_username(self, user_name):
        count = 3
        while count:
            try:
                if user_name == 'Гость':
                    check_user_name = input(
                        'Введите своё имя: '
                    ).strip() or f'Гость_{randint(1, 1000)}'
                else:
                    check_user_name = user_name
                if len(check_user_name) > 25:
                    raise UsernameToLongError
                return check_user_name
            except UsernameToLongError as ce:
                self.__logger.info(ce)
                print(ce)
            finally:
                count -= 1
        else:
            info_msg = 'Превышено максимальное количество попыток ввода.'
            self.__logger.info(info_msg)
            print(info_msg)
            exit(0)

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
                self.__logger.info(f'Отправлено: {str(request)}.')
                response = get_message(self._sock)
                response = self.translate_response(response)
                self.__logger.info(f'Получено: {str(response)}.')
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            info_msg = 'Клиент закрыт по инициативе пользователя.'
            self.__logger.info(info_msg)
            print(info_msg)
        except (ConnectionResetError, OSError):
            info_msg = 'Соединение с сервером разорвано.'
            self.__logger.warning(info_msg)
            print(info_msg)
        except CUSTOM_EXCEPTIONS as ce:
            self.__logger.error(ce)
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
        'port', nargs='?', default=f'{DEFAULT_PORT}', type=int,
        help='порт сервера'
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
            f'argument port: invalid choice: {result.port} '
            f'(choose from 1024-65535)'
        )
    return result


def run():
    args = parse_args()
    client = Client((args.addr, args.port), args.user)
    client.main_loop()


if __name__ == '__main__':
    run()
