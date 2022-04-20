import logging
import random
import time
from aiogram import executor, types, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
from mysql import DBConnect
from emoji import emojize
from collections import defaultdict
from keyboard_menu import GetKeyboard
import order

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

get_keyboard = GetKeyboard()


async def update_num_text(message: types.Message, product_ls: str):
    db = DBConnect()
    product = db.take_product_info(product_ls)
    user_data[message.chat.id].append(product[1])
    user_data[message.chat.id].append(product[3])
    await message.answer(f"Добавили в кошик {product[1]} + 1",
                         reply_markup=get_keyboard.menu_keyboard(message.chat.id, 1, product[3]))



@dp.message_handler(Text(startswith=['В кошику']))
async def bag(message: types.Message):
    bag = order.get_total(user_data.get(message.chat.id, 0))


    await bot.send_message(message.chat.id, f'Ваше замовлення:\n {bag}', reply_markup=get_keyboard.create_order())


@dp.callback_query_handler(Text(startswith=["enter", "cancel"]))
async def create_order(call: types.CallbackQuery):
    if call.data == "enter":

        text = emojize('Замовлення прийняте:white_check_mark:\nОчікуйте повідомлення про готовність:speech_balloon:', language='alias')
        order.db_create_order(order.generate_number(), call.from_user.id, user_data.get(call.from_user.id, 0))
        #db.create_order(order.generate_number(), call.from_user.id, user_data.get(call.from_user.id, 0))
        get_keyboard.clear_bag(call.from_user.id)
        user_data[call.from_user.id].clear()
    else:
        text = emojize("Замовлення скасоване:x:", language='alias')
        get_keyboard.clear_bag(call.from_user.id)
        user_data[call.from_user.id].clear()
    await bot.answer_callback_query(
        call.id,
        text=text, show_alert=True)
    await call.message.answer('Бажаєте ще щось?', reply_markup=get_keyboard.menu_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(Text(startswith=["hot_", "ice_", "taste_"]))
async def callbacks_num(call: types.CallbackQuery):
    print(call.data)
    await update_num_text(call.message, call.data)
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message: types.message):
    caption = emojize(
        'Вас вітає Cafe YumYum :heart: \nОберіть потрібний пункт меню:mag_right:\nСподіваємся Вам в нас сподобається, бажаєм гарно провести час!:blush:',
        language='alias')
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/cafe_logo.png', 'rb'),
                         reply_markup=get_keyboard.main_menu_keyboard())


@dp.message_handler(Text(endswith=['Назад']))
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




# bot.send_message(message.chat.id, f'Hi {message.text}')
# message.chat["first_name"]

if __name__ == "__main__":
    executor.start_polling(dp)
