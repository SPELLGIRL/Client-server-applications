'''
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла
по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''

import locale

resource = ['сетевое программирование', 'сокет', 'декоратор']

# Создаем файл
with open('test_file.txt', 'w+') as test_file:
    for i in resource:
        test_file.write(i + '\n')

print(test_file)  # печатаем объект файла, что бы узнать его кодировку

file_coding = locale.getpreferredencoding()

print(f'По умолчанию кодировка - {file_coding}')

# Читаем из файла
try:
    with open('test_file.txt', 'r', encoding='utf-8') as test_file:
        for i in test_file:
            print('=' * 10, 'Содержимое файла', '=' * 10)
            print(i, end='')
except UnicodeDecodeError as e:
    print(f'Получаем ошибку:\n{e}')
