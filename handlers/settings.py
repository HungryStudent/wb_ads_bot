from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text

import keyboards.user as user_kb
from create_bot import dp
from utils import db


@dp.callback_query_handler(text="settings")
async def show_settings(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    gender_text = ["Не указан", "Мужской", "Женский"]
    await call.message.edit_text(f"""Текущие настройки
Регион: {user['name']}
Пол: {gender_text[user['gender']]}""", reply_markup=user_kb.settings)


@dp.callback_query_handler(text="change_gender")
async def start_change_gender(call: CallbackQuery):
    await call.message.edit_text("Выберите пол", reply_markup=user_kb.gender)


@dp.callback_query_handler(Text(startswith="choose_gender"))
async def change_gender(call: CallbackQuery):
    gender_id = call.data.split(":")[1]
    db.change_gender(call.from_user.id, gender_id)
    await call.message.edit_text("Пол изменен", reply_markup=user_kb.settings)


@dp.callback_query_handler(text="change_city")
async def start_change_city(call: CallbackQuery):
    await call.message.edit_text("Выберите пол", reply_markup=user_kb.get_cities())


@dp.callback_query_handler(Text(startswith="choose_city"))
async def change_city(call: CallbackQuery):
    city_id = call.data.split(":")[1]
    db.change_city(call.from_user.id, city_id)
    await call.message.edit_text("Город изменен", reply_markup=user_kb.settings)
