'''
3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе
'''

word_1 = b'attribute'
# word_2 = b'класс'
# word_3 = b'функция'
word_4 = b'type'

print(type(word_1))
print(type(word_4))

# на строки записанные на кириллице вылетает исключение
'''File "C:/Users/antonina.kletskina/Desktop/Client-server applications/Homework1/3.py", line 8
    word_2 = b'класс'
            ^
SyntaxError: bytes can only contain ASCII literal characters.'''


