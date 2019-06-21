'''
Преобразовать слова «разработка», «администрирование», «protocol», «standard»
из строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
'''

list = ['разработка', 'администрирование', 'protocol', 'standard']

for i in list:
    word_enc = i.encode('utf-8')
    word_dec = bytes.decode(word_enc, 'utf-8')
    print(f'слово - {word_enc} имеет тип данных -{type(word_enc)}')
    print(f'слово - {word_dec} имеет тип данных -{type(word_dec)}\n')
