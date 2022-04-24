from collections import defaultdict
from emoji import emojize
from aiogram import executor, types, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
from mysql import DBConnect


class GetKeyboard:

    def __init__(self):
        self.value = defaultdict(list)
        self.price = defaultdict(list)
        self.db = DBConnect()

    def clear_bag(self, chat_id: int):
        self.value[chat_id].clear()
        self.price[chat_id].clear()

    def menu_keyboard(self, chat_id: int, value: int = 0, price: int = 0):
        self.value[chat_id].append(value)
        self.price[chat_id].append(price)
        self.bag = f'В кошику {sum(self.value[chat_id])} товарів, до оплати {sum(self.price[chat_id])} грн.'
        self.buttons = [emojize('Гарячі напої:coffee:', language='alias'),
                        emojize('Холодні напої:tropical_drink:', language='alias'),
                        emojize('Десерти:cake:', language='alias')
                        ]
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
            *self.buttons
        ).add(self.bag).row(emojize(':rewind:Назад', language='alias'))
        return self.keyboard

    def main_menu_keyboard(self):
        self.buttons = [emojize('Меню:clipboard:', language='alias'),
                        emojize('Залишити відгук:pencil2:', language='alias'),
                        emojize('Про нас:postbox:', language='alias')]
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        self.keyboard.add(*self.buttons)
        return self.keyboard

    def hot_buttons(self):
        button = []
        for product_name, product_ls, price in self.db.product_hot():
            button.append(types.InlineKeyboardButton(text=f"{product_name} - {price} грн", callback_data=f"{product_ls}"))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*button)
        return keyboard

    def ice_buttons(self):
        button = []
        for product_name, product_ls, price in self.db.product_ice():
            button.append(
                types.InlineKeyboardButton(text=f"{product_name} - {price} грн", callback_data=f"{product_ls}"))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*button)
        return keyboard

    def taste_buttons(self):
        button = []
        for product_name, product_ls, price in self.db.product_taste():
            button.append(
                types.InlineKeyboardButton(text=f"{product_name} - {price} грн", callback_data=f"{product_ls}"))
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*button)
        return keyboard

    def create_order(self):
        self.buttons = [
            types.InlineKeyboardButton(text=emojize("Підтвердити:white_check_mark:", language='alias'),
                                       callback_data="enter"),
            types.InlineKeyboardButton(text=emojize("Скасувати:x:", language='alias'), callback_data="cancel")
        ]
        self.keyboard = types.InlineKeyboardMarkup(row_width=2)
        self.keyboard.add(*self.buttons)
        return self.keyboard

    def hide_bag_buttons(self):
        self.buttons = [
            types.InlineKeyboardButton(text=emojize(":ok_hand:", language='alias'),
                                       callback_data="pass")
        ]
        self.keyboard = types.InlineKeyboardMarkup(row_width=1)
        self.keyboard.add(*self.buttons)
        return self.keyboard

    def admin_keyboard(self):
        self.buttons = [emojize('Нові замовлення>:bell:', language='alias'),
                        emojize('Статистика за день:bar_chart:', language='alias')]
        self.keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        self.keyboard.add(*self.buttons)
        return self.keyboard

    def admin_orders(self):
        button = []
        # for product_name in self.db.take_new_orders():
        button = [
                types.InlineKeyboardButton(text=emojize("Виконано:white_check_mark:", language='alias'),
                                           callback_data="confirm"),
                types.InlineKeyboardButton(text=emojize("Скасувати:x:", language='alias'), callback_data="delete")
            ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*button)
        return keyboard
