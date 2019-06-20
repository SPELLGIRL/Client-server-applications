'''
5.  Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты
из байтовового в строковый тип на кириллице.
'''

import subprocess

ping_resurs = [['ping', 'yandex.ru'], ['ping', 'youtube.com']]

for ping in ping_resurs:

    ping_process = subprocess.Popen(ping, stdout=subprocess.PIPE)

    for line in ping_process.stdout:
            # print(line)
            line = line.decode('cp866').encode('utf-8')
            print(line.decode('utf-8'), end='')

