from aiogram import executor, types, Dispatcher, Bot
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from collections import defaultdict
from keyboard_menu import GetKeyboard
from mysql import DBConnect
from emoji import emojize
import order
import logging
import time

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot('5397776041:AAF0n0GYOqe0rLIL5G4tLbX0f2RDbiQ1xmU')
dp = Dispatcher(bot=bot, storage=storage)

user_data = defaultdict(list)

get_keyboard = GetKeyboard()


class Form(StatesGroup):
      reviews = State()

@dp.message_handler(commands=['start'])
async def start(message: types.message):
    db = DBConnect()
    db.create_customers(message.from_user)
    caption = emojize(
        'Вас вітає Cafe YumYum :heart: \nОберіть потрібний пункт меню:mag_right:\nСподіваємся Вам в нас сподобається, бажаєм гарно провести час!:blush:',
        language='alias')
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/cafe_logo.png', 'rb'),
                         reply_markup=get_keyboard.main_menu_keyboard())


@dp.message_handler(Text(startswith=['Меню']))
async def main_menu(message: types.Message):
    caption = 'Переходь до потрібного пункту меню та замовляй смачненьке!)\n Коли обереш потрібне тисни на кошик'
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/main_menu.jpg', 'rb'),
                         reply_markup=get_keyboard.menu_keyboard(message.chat.id))


@dp.message_handler(Text(startswith=['Гарячі напої']))
async def menu_hot(message: types.Message):
    caption = emojize('Обирай що до смаку:coffee:', language='alias')
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/hot_menu.jpg', 'rb'),
                         reply_markup=get_keyboard.hot_buttons())


@dp.message_handler(Text(startswith=['Холодні напої']))
async def menu_ice(message: types.Message):
    caption = emojize('Обирай що до смаку:tropical_drink:', language='alias')
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/ice_menu.jpg', 'rb'),
                         reply_markup=get_keyboard.ice_buttons())


@dp.message_handler(Text(startswith=['Десерти']))
async def menu_taste(message: types.Message):
    caption = emojize('Обирай що до смаку:cake:', language='alias')
    await bot.send_photo(message.chat.id, caption=caption, photo=open('images/taste_menu.jpg', 'rb'),
                         reply_markup=get_keyboard.taste_buttons())


async def update_bag(message: types.Message, product_ls: str):
    db = DBConnect()
    product = db.take_product_info(product_ls)
    user_data[message.chat.id].append(product[1])
    user_data[message.chat.id].append(product[3])
    await message.answer(f"Добавили в кошик {product[1]} + 1",
                         reply_markup=get_keyboard.menu_keyboard(message.chat.id, 1, product[3]))


@dp.callback_query_handler(Text(startswith=["hot_", "ice_", "taste_"]))
async def callbacks_num(call: types.CallbackQuery):
    await update_bag(call.message, call.data)
    await call.answer()


@dp.message_handler(Text(startswith=['В кошику']))
async def bag(message: types.Message):
    bag = order.get_total(user_data.get(message.chat.id, 0))
    await bot.send_message(message.chat.id, f'Ваше замовлення:\n {bag}', reply_markup=get_keyboard.create_order())


@dp.callback_query_handler(Text(startswith=["enter", "cancel"]))
async def create_order(call: types.CallbackQuery):
    if call.data == "enter":
        order_number = order.generate_number()
        message_info = f'Ваш номер замовлення №{order_number}\nБажаєте ще щось?'
        text = emojize(f'Ваше замовлення №{order_number} прийняте:white_check_mark:\nОчікуйте повідомлення про готовність:speech_balloon:', language='alias')
        order.db_create_order(order_number, call.from_user.id, user_data.get(call.from_user.id, 0))
        get_keyboard.clear_bag(call.from_user.id)
        user_data[call.from_user.id].clear()
    else:
        text = emojize("Замовлення скасоване:x:", language='alias')
        get_keyboard.clear_bag(call.from_user.id)
        user_data[call.from_user.id].clear()
        message_info = 'Замовлення скасоване:x:'
    await bot.answer_callback_query(call.id, text=text, show_alert=True)
    await call.message.edit_reply_markup(reply_markup=get_keyboard.hide_bag_buttons())
    await call.message.answer(emojize(message_info, language='alias'), reply_markup=get_keyboard.menu_keyboard(call.from_user.id))
    await call.answer()


@dp.callback_query_handler(Text(startswith=["pass"]))
async def pass_message(call: types.CallbackQuery):
    message_info = "Кошик вже порожній:("
    await call.message.answer(emojize(message_info, language='alias'))
    await call.answer()


@dp.message_handler(Text(endswith=['Назад']))
async def back_main_menu(message: types.Message):
    await start(message)


@dp.message_handler(Text(startswith=['Про нас']))
async def about(message: types.Message):
    await message.answer("Cafe YumYum\nАдреса: м.Київ\nКонтакти для звязку: test@test")


@dp.message_handler(Text(startswith=['Залишити відгук']))
async def about(message: types.Message):
    await Form.reviews.set()
    markup = types.ReplyKeyboardRemove()
    await message.answer("Напишіть Ваш відгук:", reply_markup=markup)


@dp.message_handler(state=Form.reviews)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['reviews'] = message.text
    db = DBConnect()
    db.create_reviews(message.chat.id, md.text(data['reviews']))
    await message.reply("Дякуєм за Ваш відгук!", reply_markup=get_keyboard.main_menu_keyboard())
    await state.finish()


@dp.message_handler(commands=['admin'])
async def admin_menu(message: types.message):
    db = DBConnect()
    if db.admin(message.chat.id):
        caption = 'Вітаю в панелі адміністратора!'
        await bot.send_message(message.chat.id, caption, reply_markup=get_keyboard.admin_keyboard())
    else:
        pass


@dp.message_handler(Text(startswith=['Нові замовлення>']))
async def admin_orders(message: types.Message):
    db = DBConnect()
    all_new_orders = db.take_new_orders()
    if len(all_new_orders) == 0:
        await message.answer('Нових замовлень немає')
    else:
        for el in all_new_orders:
            order = []
            order_price = []
            for name, price, _, number in db.take_order_info(el):
                order_price.append(int(price))
                order.append(f"Товар: {name} (1шт) - {price} грн.")
            order.append(f'Загальна сумма замовлення {sum(order_price)}')
            order.append(f'Номер замовлення клієнта {el}')
            await message.answer('\n'.join(order), reply_markup=get_keyboard.admin_orders())


@dp.callback_query_handler(Text(startswith=["confirm", "delete"]))
async def admin_order_status(call: types.CallbackQuery):
    db = DBConnect()
    order_number = int(call.message.text[len(call.message.text)-12:])
    if call.data == "confirm":
        db.edit_status(order_number, "confirm")
        user = db.take_user_id(order_number)
        await bot.send_message(user, f'Ваше замовлення №{order_number} вже готове!')
    else:
        db.edit_status(order_number, "cancel")
    await call.message.edit_reply_markup(reply_markup=get_keyboard.hide_bag_buttons())
    await call.answer()


@dp.message_handler(Text(startswith=['Статистика за день']))
async def admin_statistic(message: types.Message):
    db = DBConnect()
    all_new_orders = db.take_statistics()
    all_day_cost = []
    if len(all_new_orders) == 0:
        await message.answer('Сьогодні замовлень немає')
    else:
        for el in all_new_orders:
            order = []
            order_price = []
            for name, price, _, number in db.take_order_info(el):
                order_price.append(int(price))
                order.append(f"Товар: {name} (1шт) - {price} грн.")
            order.append(f'Загальна сумма замовлення {sum(order_price)}')
            order.append(f'Номер замовлення клієнта {el}')
            all_day_cost.append(sum(order_price))
            await message.answer('\n'.join(order))
        await message.answer(f'\nЗагальна виручка за сьогодні: {sum(all_day_cost)} грн.')


if __name__ == "__main__":
    executor.start_polling(dp)
