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
#якшо будем приймати ще код товару то треба буде поміняти логіку



#dct містить ід клієнта і список кодів товарів в замовленні(або весь список потім туту розберу)
#має приходити номер замовлення згенерований раніше і список кодів товарів. треба добавляти окремо кожний код товару до одного замовлення
def db_create_order(order_number: int, user_id: int, order_info: list):
    db = DBConnect()
    # for el in order_info:
    #     if type(el) == str:
    #         db.product_id(el)
    #     else: pass
    db.create_order(order_number,user_id)
    #для Order  order_n  и cust_id
    #product in order  Orer_n Product_id
    # print(order_number)
    # print(user_id)
    # print(order_info)
    return


def generate_number():
    times = str(time.time_ns())
    order_number = times[2:12]
    num = int(order_number)
    return num



if __name__ == "__main__":
    generate_number()


