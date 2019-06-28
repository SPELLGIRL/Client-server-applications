"""
Функции ​​сервера:​
- принимает ​с​ообщение ​к​лиента;
- формирует ​​ответ ​к​лиенту;
- отправляет ​​ответ ​к​лиенту;
- имеет ​​параметры ​к​омандной ​с​троки:
- -p ​​<port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт ​​8000);
- -a ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса).
"""
from argparse import ArgumentParser
from settings import DEFAULT_PORT, DEFAULT_IP, MAX_CONNECTIONS, TIMEOUT
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import get_message, send_message
from jim.config import *


class Server:
    def __init__(self):
        self._host = args.a
        self._port = args.p
        self._connections = []
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.bind((self._host, self._port))
        self._sock.listen(MAX_CONNECTIONS)
        self._sock.settimeout(TIMEOUT)
        print(
            f'Сервер запущен (слушает с адреса: {self._host or "любой"}, порт: {self._port})')

    def connect(self):
        try:
            client, addr = self._sock.accept()
        except OSError:
            pass
        else:
            print(f'Получен запрос на соединение от {addr[0]}:{addr[1]}')
            self._connections.append(client)
            if len(self._connections) > MAX_CONNECTIONS:
                self.disconnect(client)

    def disconnect(self, client):
        addr, port = client.getpeername()
        print(f'Соединение с клиентом {addr}:{port} разорвано.')
        if client in self._connections:
            self._connections.remove(client)
        client.close()

    def validate_request(self, client):
        try:
            request = get_message(client)
            print(request)
        except ConnectionResetError:
            self.disconnect(client)
        except (ValueError, TypeError):
            print('Принято некорретное сообщение от клиента.')
            self.disconnect(client)
        else:
            return request

    def validate_response(self, client, response):
        try:
            if ACTION in response and \
                    response[ACTION] == PRESENCE and \
                    TIME in response and \
                    isinstance(response[TIME], float):
                response = {RESPONSE: 200}
            else:
                response = {RESPONSE: 400, ERROR: 'Не верный запрос.'}
            send_message(client, response)
        except ConnectionResetError:
            self.disconnect(client)

    def main_loop(self):
        try:
            while True:
                self.connect()
                for connection in self._connections:
                    request = self.validate_request(connection)
                    if request:
                        if connection in self._connections:
                            self.validate_response(connection, request)
        except KeyboardInterrupt:
            print('Сервер остановлен по инициативе пользователя.')


if __name__ == '__main__':
    parser = ArgumentParser(description='Запуск сервера.')
    parser.add_argument(
        '-a', nargs='?', default=f'{DEFAULT_IP}', type=str,
        help='прослушиваемые IP адреса'
    )
    parser.add_argument(
        '-p', nargs='?', default=f'{DEFAULT_PORT}', type=int,
        help='порт сервера в диапазоне от 1024 до 65535'
    )
    args = parser.parse_args()
    if args.p not in range(1024, 65535):
        parser.error(f'argument -p: invalid choice: {args.p} (choose from 1024-65535)')

    server = Server()
    server.main_loop()
