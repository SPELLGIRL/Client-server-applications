import socket
from jim.utils import Message, receive
from jim.config import *
from exceptions import *
from client import log_decorator
import time


class Console:
    __slots__ = ('__client', '__actions')

    def __init__(self, client):
        self.__client = client

        self.__actions = (
            {
                ACTION: 'exit',
                'name': 'Выйти',
            },
            {
                ACTION: SEND_MSG,
                'name': 'Отправить сообщение(* - всем)',
                'params': (TO, TEXT,)
            },
            {
                ACTION: READ_MESSAGES,
                'name': 'Открыть режим чтения(выход Ctrl-C)',
            },
            {
                ACTION: GET_CONTACTS,
                'name': 'Запросить список контактов',
            },
        )

    @log_decorator
    def interact(self):
        while True:
            try:
                num = abs(int(input(' | '.join([f'{key}. {action["name"]}' for key, action in enumerate(self.__actions, 0)]) + ' | Выберите действие: ')))
                if 0 <= num <= len(self.__actions):
                    start = self.__actions[num]
                else:
                    raise ValueError
                if start[ACTION] == 'exit':
                    raise KeyboardInterrupt
                params = {ACTION: start[ACTION]}
                if start[ACTION] == READ_MESSAGES:
                    self.receiver()
                    continue
                if 'params' in start:
                    for param in start['params']:
                        p = str(input(f'Выберите параметр "{param}": '))
                        params[param] = p
                break
            except ValueError:
                pass
        return Message(**params)

    def main(self):
        try:
            while True:
                message = self.interact()
                self.__client.send(message)
                time.sleep(1)
                self.receiver(flag=0)
        except KeyboardInterrupt:
            print('Клиент закрыт по инициативе пользователя.')
        except ConnectionResetError:
            print('Соединение с сервером разорвано.')
        except CUSTOM_EXCEPTIONS as ce:
            print(ce)
        finally:
            self.__client.close()

    def receiver(self, flag=1):
        try:
            while True:
                messages = []
                try:
                    messages = receive(self.__client.sock, self.__client.logger)
                except socket.timeout:
                    pass
                while len(messages):
                    message = messages.pop()
                    checked_msg = self.__client.check_response(message)
                    self.receive_callback(checked_msg)
                if flag != 1:
                    break
        except KeyboardInterrupt:
            pass

    @staticmethod
    def receive_callback(response):
        if isinstance(response, str):
            print(response)
        if response.action == GET_CONTACTS:
            if response.quantity:
                print(f'Список контактов (подключено {response.quantity}).')
            if response.user:
                print(f'{response.user or "Нет данных"}')
        elif response.action == SEND_MSG:
            if response.sender != response.destination:
                print(f'Сообщение от {response.sender}: {response.text}')
        return response


class Gui:
    __slots__ = ('__client',)

    def __init__(self, client):
        self.__client = client
        pass

    def run(self):
        pass
