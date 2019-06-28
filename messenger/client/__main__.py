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
from argparse import ArgumentParser
from settings import DEFAULT_PORT, DEFAULT_IP
from socket import socket, AF_INET, SOCK_STREAM
from exceptions import UsernameToLongError, ResponseCodeLenError, \
    MandatoryKeyError, \
    ResponseCodeError
from jim.config import *
from jim.utils import send_message, get_message


class Client:
    def __init__(self):
        self._host = args.addr
        self._port = args.port
        self._username = input("Введите своё имя: ") or "Гость"
        if len(self._username) > 25:
            raise UsernameToLongError(self._username)
        self._sock = socket(AF_INET, SOCK_STREAM)
        try:
            self._sock.connect((self._host, self._port))
        except ConnectionRefusedError:
            print('Сервер отклонил запрос на подключение.')
            exit(1)
        print(
            f'Клиент запущен (сервер: {self._host}:{self._port})')

    def create_presence(self):
        message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self._username
            }
        }
        return message

    @staticmethod
    def get_validate_response(server):
        response = get_message(server)
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

    def main_loop(self):
        try:
            while True:
                msg = self.create_presence()
                send_message(self._sock, msg)
                response = self.get_validate_response(self._sock)
                print(response)
        except KeyboardInterrupt:
            print('Клиент закрыт по инициативе пользователя.')
        except ConnectionResetError:
            print('Соединение с сервером разорвано.')
        finally:
            self._sock.close()


if __name__ == '__main__':
    parser = ArgumentParser(description='Запуск клиента.')
    parser.add_argument(
        'addr', nargs='?', default=f'{DEFAULT_IP}', type=str,
        help='IP адрес сервера'
    )
    parser.add_argument(
        'port', nargs='?', default=f'{DEFAULT_PORT}', type=int, help='порт сервера'
    )
    args = parser.parse_args()
    if args.port not in range(1024, 65535):
        parser.error(f'argument port: invalid choice: {args.port} (choose from 1024-65535)')

    client = Client()
    client.main_loop()
