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
    def __init__(self, address):
        self._connections = []
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.bind(address)
        self._sock.listen(MAX_CONNECTIONS)
        self._sock.settimeout(TIMEOUT)
        print(f'Сервер запущен ({address[0] or "*"}:{address[1]}).')

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

    @staticmethod
    def create_response(request):
        if ACTION in request and \
                request[ACTION] == PRESENCE and \
                TIME in request and \
                isinstance(request[TIME], float):
            return {RESPONSE: 200}
        else:
            return {RESPONSE: 400, ERROR: 'Не верный запрос.'}

    def main_loop(self):
        try:
            while True:
                self.connect()
                for client in self._connections:
                    try:
                        request = get_message(client)
                        print(request)
                        if request:
                            if client in self._connections:
                                response = self.create_response(request)
                                send_message(client, response)
                    except ConnectionResetError:
                        self.disconnect(client)
                    except (ValueError, TypeError):
                        print('Принято некорретное сообщение от клиента.')
                        self.disconnect(client)
        except KeyboardInterrupt:
            print('Сервер остановлен по инициативе пользователя.')

    def close(self):
        self._sock.close()


def parse_args():
    parser = ArgumentParser(description='Запуск сервера.')
    parser.add_argument(
        '-a', nargs='?', default=f'{DEFAULT_IP}', type=str,
        help='ip адрес интерфейса (по умолчанию любой)'
    )
    parser.add_argument(
        '-p', nargs='?', default=f'{DEFAULT_PORT}', type=int,
        help='порт сервера в диапазоне от 1024 до 65535'
    )
    result = parser.parse_args()
    if result.p not in range(1024, 65535):
        parser.error(
            f'argument -p: invalid choice: {result.p} (choose from 1024-65535)'
        )
    return result


def run():
    args = parse_args()
    server = Server((args.a, args.p))
    server.main_loop()


if __name__ == '__main__':
    run()
