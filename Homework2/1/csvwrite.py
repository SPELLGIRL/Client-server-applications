"""
1.	Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV.
Для этого:
a.	Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений
извлечь значения параметров «Изготовитель системы»,  «Название ОС»,
«Код продукта», «Тип системы». Значения каждого параметра поместить
в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных
отчета — например, main_data — и поместить в него названия столбцов отчета
в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
«Тип системы». Значения для этих столбцов также оформить в виде списка
и поместить в файл main_data (также для каждого файла);
b.	Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
c.	Проверить работу программы через вызов функции write_to_csv().
"""

import os
import csv
import re


def get_data() -> list:
    """
    Функция запрашивает информацию о системе из каждого файла в папке 'src'
    и сортирует данные в необходимом порядке.
    :return: Список с отсортированными данными.
    """
    src_dir = os.path.join(os.getcwd(), 'src')
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    info = {
        'Изготовитель системы': os_prod_list,
        'Название ОС': os_name_list,
        'Код продукта': os_code_list,
        'Тип системы': os_type_list,
    }

    for srcfile in os.listdir(src_dir):
        with open(os.path.join(src_dir, srcfile), 'r') as f_in:
            for read_string in f_in:
                match = re.search(r'([^:]*):\s*(.*)', read_string)
                if match and (match[1] in info.keys()):
                    info[match[1].strip()].append(match[2].strip())

    for i in info.values():
        main_data.append(i)
    main_data = [i for i in zip(*main_data)]
    main_data.insert(0, list(info.keys()))
    return main_data


def write_to_csv(filename: str) -> None:
    """
    Функция записывает переданный список данных в файл.
    :param filename: Имя файла.
    :return: None
    """
    data = get_data()
    with open(os.path.join(os.getcwd(), filename), 'w',
              encoding='utf-8') as f_out:
        f_n_writer = csv.writer(f_out, quoting=csv.QUOTE_NONNUMERIC)
        f_n_writer.writerows(data)


if __name__ == '__main__':
    write_to_csv('result.csv')
