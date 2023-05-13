from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils import db

search_data = CallbackData("search", "direction", "max_page", "page", "query")
article_data = CallbackData("article", "direction", "max_page", "page", "query")
catalog_data = CallbackData("catalog", "direction", "max_page", "page", "query")

menu = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("🔎 Реклама в поиске", callback_data="ads_in_search"),
                                             InlineKeyboardButton("🃏 Реклама в карточке", callback_data="ads_in_card"),
                                             InlineKeyboardButton("🗂️ Ставки в каталоге",
                                                                  callback_data="ads_in_catalog"),
                                             InlineKeyboardButton("⚙ Настройки", callback_data="settings"))

back_to_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

check_sub = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Проверить подписку", callback_data="check_sub"))

settings = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Изменить пол", callback_data="change_gender"),
                                                 InlineKeyboardButton("Изменить регион", callback_data="change_city"),
                                                 InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))

gender = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Не указан", callback_data="choose_gender:0")).add(
    InlineKeyboardButton("Мужской", callback_data="choose_gender:1"),
    InlineKeyboardButton("Женский", callback_data="choose_gender:2"),
    InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))


def get_cities():
    kb = InlineKeyboardMarkup(row_width=1)
    cities = db.get_cities()
    for city in cities:
        kb.add(InlineKeyboardButton(city["name"], callback_data=f"choose_city:{city['id']}"))
    kb.add(InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))
    return kb


def get_search(products_count, page, query):
    max_page = products_count // 7
    if products_count % 7 != 0:
        max_page += 1
    return InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("⬅", callback_data=search_data.new("left", max_page, page - 1, query)),
        InlineKeyboardButton(f"{page}/{max_page}", callback_data="empty"),
        InlineKeyboardButton("➡", callback_data=search_data.new("right", max_page, page + 1, query)),
        InlineKeyboardButton("🔄 Обновить ставки", callback_data=search_data.new("none", max_page, page, query))).add(
        InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))


def get_article(products_count, page, query):
    max_page = products_count // 7
    if products_count % 7 != 0:
        max_page += 1
    return InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("⬅", callback_data=article_data.new("left", max_page, page - 1, query)),
        InlineKeyboardButton(f"{page}/{max_page}", callback_data="empty"),
        InlineKeyboardButton("➡", callback_data=article_data.new("right", max_page, page + 1, query)),
        InlineKeyboardButton("🔄 Обновить ставки", callback_data=article_data.new("none", max_page, page, query))).add(
        InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))


def get_catalog(products_count, page, query):
    max_page = products_count // 7
    if products_count % 7 != 0:
        max_page += 1
    return InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("⬅", callback_data=catalog_data.new("left", max_page, page - 1, query)),
        InlineKeyboardButton(f"{page}/{max_page}", callback_data="empty"),
        InlineKeyboardButton("➡", callback_data=catalog_data.new("right", max_page, page + 1, query)),
        InlineKeyboardButton("🔄 Обновить ставки", callback_data=catalog_data.new("none", max_page, page, query))).add(
        InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))


def get_categories_for_catalog(categories):
    kb = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        kb.add(InlineKeyboardButton(category["name"], callback_data=f"get_catalog_info:{category['id']}"))
    kb.add(InlineKeyboardButton("🔄 Попробовать заново", callback_data="ads_in_catalog"),
           InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))
    return kb


def get_main_catalog(catalog):
    kb = InlineKeyboardMarkup(row_width=1)
    for product in catalog:
        kb.add(InlineKeyboardButton(product["name"], callback_data=f"select_catalog:{product['id']}"))
    kb.add(InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))
    return kb


def get_catalog_childs(catalog_childs):
    kb = InlineKeyboardMarkup(row_width=1)
    for catalog_child in catalog_childs:
        kb.add(InlineKeyboardButton(catalog_child["name"], callback_data=f"select_catalog_child:{catalog_child['id']}"))
    kb.add(InlineKeyboardButton("⏪️ Главное меню", callback_data="back_to_menu"))
    return kb
