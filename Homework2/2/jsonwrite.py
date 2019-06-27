"""
2.	Задание на закрепление знаний по модулю json. Есть файл orders в формате
JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение
данными. Для этого:
a.	Создать функцию write_order_to_json(), в которую передается 5
параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись данных
в виде словаря в файл orders.json. При записи данных указать величину отступа
в 4 пробельных символа;
b.	Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.
"""

import os
import json


def write_order_to_json(item: str, quantity: str, price: str, buyer: str,
                        date: str) -> None:
    """
    Функция дополняет файл orders.json переданными данными.
    :param item: Наименование товара
    :param quantity: Количество товара
    :param price: Цена товара
    :param buyer: Покупатель
    :param date: Дата
    :return: None
    """
    with open(os.path.join(os.getcwd(), 'orders.json'), 'r',
              encoding='utf-8') as f_in:
        data = json.load(f_in)
    with open(os.path.join(os.getcwd(), 'orders.json'), 'w',
              encoding='utf-8') as f_out:
        order = {
            "item": item,
            "quantity": quantity,
            "price": price,
            "buyer": buyer,
            "date": date,
        }
        data['orders'].append(order)
        json.dump(data, f_out, indent=4)


if __name__ == '__main__':
    write_order_to_json('Cheer', '2', '4500 RUB', 'Antonina', '2019-06-25')
    write_order_to_json('Macbook', '1', '150000 RUB', 'Antonina', '2019-06-25')
