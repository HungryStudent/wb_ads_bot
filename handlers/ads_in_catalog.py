from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
import keyboards.user as user_kb
from create_bot import dp
from utils import db, wb


@dp.callback_query_handler(text="ads_in_catalog")
async def enter_query_for_catalog(call: CallbackQuery):
    catalog = db.get_catalog()
    await call.message.edit_text("""Выберите категорию из каталога:""", reply_markup=user_kb.get_main_catalog(catalog))


@dp.callback_query_handler(Text(startswith="select_catalog:"))
async def select_catalog(call: CallbackQuery):
    catalog_id = int(call.data.split(":")[1])
    catalog_childs = db.get_catalog_childs(catalog_id)
    await call.message.edit_text("Выберите подкатегорию:", reply_markup=user_kb.get_catalog_childs(catalog_childs))


@dp.callback_query_handler(Text(startswith="select_catalog_child:"))
async def select_catalog_child(call: CallbackQuery):
    catalog_child_id = int(call.data.split(":")[1])
    catalog = db.get_catalog_by_id(catalog_child_id)
    user = db.get_user(call.from_user.id)
    data = wb.get_catalog(catalog_child_id, curr_page=1, city=user["city_code"])
    if data is None:
        await call.message.edit_text(
            f'Ставки по категории: "{catalog["name"]}" не найдены.',
            reply_markup=user_kb.back_to_menu)
        return
    await call.message.edit_text(data["msg_text"],
                                 reply_markup=user_kb.get_catalog(data["products_count"], 1, catalog_child_id))


@dp.callback_query_handler(user_kb.catalog_data.filter())
async def flip_catalog(call: CallbackQuery, callback_data: dict):
    if int(callback_data["page"]) == 0:
        await call.answer("Вы на первой странице")
        return
    elif int(callback_data["page"]) == int(callback_data["max_page"]) + 1:
        await call.answer("Вы на последней странице")
        return
    user = db.get_user(call.from_user.id)
    data = wb.get_catalog(int(callback_data["query"]), int(callback_data["page"]), user["city_code"])
    if data is None:
        catalog = db.get_catalog_by_id(int(callback_data["query"]))
        await call.message.edit_text(
            f'Ставки по категории: "{catalog["name"]}" не найдены.',
            reply_markup=user_kb.back_to_menu)
    else:
        await call.message.edit_text(data["msg_text"],
                                     reply_markup=user_kb.get_catalog(int(data["products_count"]),
                                                                      int(callback_data["page"]),
                                                                      int(callback_data["query"])))
