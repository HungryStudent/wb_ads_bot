from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text

import keyboards.user as user_kb
from create_bot import dp
from utils import db


@dp.message_handler(text="⚙ Настройки")
async def show_settings(message: Message):
    user = db.get_user(message.from_user.id)
    gender_text = ["Не указан", "Мужской", "Женский"]
    await message.answer(f"""Текущие настройки
Регион: {user['name']}
Пол: {gender_text[user['gender']]}""", reply_markup=user_kb.settings)


@dp.callback_query_handler(text="change_gender")
async def start_change_gender(call: CallbackQuery):
    await call.message.edit_text("Выберите пол", reply_markup=user_kb.gender)


@dp.callback_query_handler(Text(startswith="choose_gender"))
async def change_gender(call: CallbackQuery):
    gender_id = call.data.split(":")[1]
    db.change_gender(call.from_user.id, gender_id)
    await call.message.answer("Пол изменен", reply_markup=user_kb.menu)
    await call.message.delete()


@dp.callback_query_handler(text="change_city")
async def start_change_city(call: CallbackQuery):
    await call.message.edit_text("Выберите пол", reply_markup=user_kb.get_cities())


@dp.callback_query_handler(Text(startswith="choose_city"))
async def change_city(call: CallbackQuery):
    city_id = call.data.split(":")[1]
    db.change_city(call.from_user.id, city_id)
    await call.message.answer("Город изменен", reply_markup=user_kb.menu)
    await call.message.delete()
