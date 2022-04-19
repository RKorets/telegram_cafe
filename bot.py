import logging
import random
import time
from aiogram import executor, types, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
from mysql import tableName
from emoji import emojize
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

bot = Bot('5397776041:AAF0n0GYOqe0rLIL5G4tLbX0f2RDbiQ1xmU')
dp = Dispatcher(bot=bot)


def auth(func):
    async def wrapper(message):
        if message.chat.id != 368553201:
            return await message.answer(f'You dont have rules!')
        return await func(message)

    return wrapper


user_data = defaultdict(list)


class GetKeyboard:

    def __init__(self):
        self.value = defaultdict(list)
        self.price = defaultdict(list)

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
        buttons = [
            types.InlineKeyboardButton(text="Гарячий шоколад", callback_data="hot_chook"),
            types.InlineKeyboardButton(text="Капучіно", callback_data="hot_cap"),
            types.InlineKeyboardButton(text="Латте", callback_data="hot_late"),
            types.InlineKeyboardButton(text="3 в 1", callback_data="hot_3in1"),
            types.InlineKeyboardButton(text="Американо", callback_data="hot_americano"),
            types.InlineKeyboardButton(text="Какао", callback_data="hot_cacao"),
            types.InlineKeyboardButton(text="Чай чорний", callback_data="hot_tea")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    def ice_buttons(self):
        buttons = [
            types.InlineKeyboardButton(text="Айс латте", callback_data="ice_late"),
            types.InlineKeyboardButton(text="Сік Sandora", callback_data="ice_juice"),
            types.InlineKeyboardButton(text="Лимонад", callback_data="ice_lemon"),
            types.InlineKeyboardButton(text="Вода", callback_data="ice_water"),
            types.InlineKeyboardButton(text="Coca Cola", callback_data="ice_cola")
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        return keyboard

    def taste_buttons(self):
        # buttons = []
        # for el, price, ls in get.menu():
        #   buttons.append(types.InlineKeyboardButton(text=f"{el} {price}", callback_data=f"{ls}")

        self.buttons = [
            types.InlineKeyboardButton(text="Піца Ле-Маріо", callback_data="taste_pizza"),
            types.InlineKeyboardButton(text="Паніні ковбаски", callback_data="taste_panini"),
            types.InlineKeyboardButton(text="Салат з крабів", callback_data="taste_salat"),
            types.InlineKeyboardButton(text="Картопля фрі", callback_data="taste_fry"),
            types.InlineKeyboardButton(text="Стейк", callback_data="taste_steak")
        ]
        self.keyboard = types.InlineKeyboardMarkup(row_width=1)
        self.keyboard.add(*self.buttons)
        return self.keyboard

    def create_order(self):
        self.buttons = [
            types.InlineKeyboardButton(text=emojize("Підтвердити:white_check_mark:", language='alias'),
                                       callback_data="enter"),
            types.InlineKeyboardButton(text=emojize("Скасувати:x:", language='alias'), callback_data="cancel")
        ]
        self.keyboard = types.InlineKeyboardMarkup(row_width=2)
        self.keyboard.add(*self.buttons)
        return self.keyboard


get_keyboard = GetKeyboard()


async def update_num_text(message: types.Message, one: int, action: str):
    user_data[message.chat.id].append(action)
    if action == 'cap':
        taste = 'Капучіно'
    else:
        taste = action
    await message.answer(f"Добавили в кошик {taste} + 1",
                         reply_markup=get_keyboard.menu_keyboard(message.chat.id, 1, 24))


@dp.callback_query_handler(Text(startswith=["enter", "cancel"]))
async def create_order(call: types.CallbackQuery):
    get_keyboard.clear_bag(call.from_user.id)
    user_data[call.from_user.id].clear()
    if call.data == "enter":
        text = emojize('Замовлення прийняте:white_check_mark:\nОчікуйте повідомлення про готовність:speech_balloon:', language='alias')
    else:
        text = emojize("Замовлення скасоване:x:", language='alias')
    await bot.answer_callback_query(
        call.id,
        text=text, show_alert=True)
    await call.message.answer('Бажаєте ще щось?', reply_markup=get_keyboard.menu_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(Text(startswith=["hot_", "ice_", "taste_"]))
async def callbacks_num(call: types.CallbackQuery):
    # user_value = user_data.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    # id   ls_name  name  price
    # get.db.products(call.data) - де call.data - ls товару вернути треба кортеж (name,price,ls)
    await update_num_text(call.message, 1, action)
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message: types.message):
    caption = emojize(
        'Вас вітає Cafe YumYum :heart: \nОберіть потрібний пункт меню:mag_right:\nСподіваємся Вам в нас сподобається, бажаєм гарно провести час!:blush:',
        language='alias')
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/cafe_logo.png', 'rb'),
                         reply_markup=get_keyboard.main_menu_keyboard())


@dp.message_handler(Text(startswith=['Назад']))
async def back_main_menu(message: types.Message):
    await start(message)


@dp.message_handler(Text(startswith=['Про нас']))
async def about(message: types.Message):
    await message.answer("Cafe YumYum\nАдреса: м.Київ\nКонтакти для звязку: test@test")


@dp.message_handler(Text(startswith=['Меню']))
async def main_menu(message: types.Message):
    caption = 'Переходь до потрібного пункту меню та замовляй смачненьке!)\n Коли обереш потрібне тисни на кошик'
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/cafe_logo.png', 'rb'),
                         reply_markup=get_keyboard.menu_keyboard(message.chat.id))


@dp.message_handler(Text(startswith=['Гарячі напої']))
async def menu_hot(message: types.Message):
    caption = 'Обирай що до смаку'
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/cafe_logo.png', 'rb'),
                         reply_markup=get_keyboard.hot_buttons())


@dp.message_handler(Text(startswith=['Холодні напої']))
async def menu_ice(message: types.Message):
    caption = 'Обирай що до смаку'
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/cafe_logo.png', 'rb'),
                         reply_markup=get_keyboard.ice_buttons())


@dp.message_handler(Text(startswith=['Десерти']))
async def menu_taste(message: types.Message):
    caption = 'Обирай що до смаку'
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/cafe_logo.png', 'rb'),
                         reply_markup=get_keyboard.taste_buttons())


@dp.message_handler(Text(startswith=['В кошику']))
async def bag(message: types.Message, value: int = 0, price: int = 0):
    # user_data.items()
    bag = user_data.get(message.chat.id, 0)
    await bot.send_message(message.chat.id, f'Ваше замовлення {bag}', reply_markup=get_keyboard.create_order())


# bot.send_message(message.chat.id, f'Hi {message.text}')
# message.chat["first_name"]

if __name__ == "__main__":
    executor.start_polling(dp)
