'''
2. Каждое из слов «class», «function», «method» записать в байтовом типе
без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину
соответствующих переменных.
'''

list = [b'class', b'function', b'method']

for line in list:
    print(f'тип переменной: {type(line)}')
    print(f'содержание переменной - {line}')
    print(f'длинна строки: {len(line)}\n')
