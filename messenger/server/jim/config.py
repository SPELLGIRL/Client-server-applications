"""Константы для jim протокола, настройки"""
# Ключи
# тип сообщения между клиентом и сервером
ACTION = 'action'
# время запроса
TIME = 'time'
# данные о пользователе - клиенте (вложенный словарь)
USER = 'user'
# имя пользователя - чата
ACCOUNT_NAME = 'account_name'
# код ответа
RESPONSE = 'response'
# текст ошибки
ERROR = 'error'

# Значения
PRESENCE = 'presence'

# Коды ответов
BASIC_NOTICE = 100
OK = 200
ACCEPTED = 202
WRONG_REQUEST = 400  # неправильный запрос/json объект
SERVER_ERROR = 500

# Кортеж из кодов ответов
RESPONSE_CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)
