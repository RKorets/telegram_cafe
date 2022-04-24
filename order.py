from collections import Counter
from mysql import DBConnect
import time


def get_total(bag: list):
    name = []
    total_sum = []
    for el in Counter(bag).most_common():
        if type(el[0]) == str:
            name.append(f'{el[0]}: {el[1]} шт.')
        else:
            total_sum.append(el[0]*el[1])
    name.append(f'Загальна сума до оплати: {sum(total_sum)} грн.')
    return '\n'.join(name)


def db_create_order(order_number: int, user_id: int, order_info: list):
    db = DBConnect()
    db.create_order(order_number, user_id)
    for el in order_info:
        if type(el) == str:
            db.create_product_in_order(order_number,db.product_id(el))
        else:
            pass
    return


def generate_number():
    times = str(time.time_ns())
    order_number = times[2:14]
    return order_number



if __name__ == "__main__":
    generate_number()
