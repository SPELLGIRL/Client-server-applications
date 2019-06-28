"""Все ошибки"""


# исключение. когда имя пользователя слишком длинное - более 25 символов
class UsernameToLongError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Имя пользователя {} должно быть менее 26 символов'.format(
            self.username)


# исключение. переданный код отсутствует среди стандартных кодов
class ResponseCodeError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return 'Неверный код ответа {}'.format(self.code)


# исключение. длина кода - не три символа
class ResponseCodeLenError(ResponseCodeError):
    def __str__(self):
        return 'Неверная длина кода {}. Длина кода должна быть 3 символа.'.format(
            self.code)


# исключение. отсутствует обязательный атрибут response
class MandatoryKeyError(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'Не хватает обязательного атрибута {}'.format(self.key)
