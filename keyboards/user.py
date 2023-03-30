from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils import db

search_data = CallbackData("search", "direction", "max_page", "page", "query")
article_data = CallbackData("article", "direction", "max_page", "page", "query")

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("🔎 Реклама в поиске"),
                                                                  KeyboardButton("🃏 Реклама в карточке"),
                                                                  KeyboardButton("⚙ Настройки"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

check_sub = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Проверить подписку", callback_data="check_sub"))

settings = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Изменить пол", callback_data="change_gender"),
                                                 InlineKeyboardButton("Изменить регион", callback_data="change_city"))

gender = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Не указан", callback_data="choose_gender:0")).add(
    InlineKeyboardButton("Мужской", callback_data="choose_gender:1"),
    InlineKeyboardButton("Женский", callback_data="choose_gender:2"))


def get_cities():
    kb = InlineKeyboardMarkup(row_width=1)
    cities = db.get_cities()
    for city in cities:
        kb.add(InlineKeyboardButton(city["name"], callback_data=f"choose_city:{city['id']}"))
    return kb


def get_search(products_count, page, query):
    max_page = products_count // 7
    if products_count % 7 != 0:
        max_page += 1
    return InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("⬅", callback_data=search_data.new("left", max_page, page - 1, query)),
        InlineKeyboardButton(f"{page}/{max_page}", callback_data="empty"),
        InlineKeyboardButton("➡", callback_data=search_data.new("right", max_page, page + 1, query)))


def get_article(products_count, page, query):
    max_page = products_count // 7
    if products_count % 7 != 0:
        max_page += 1
    return InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("⬅", callback_data=article_data.new("left", max_page, page - 1, query)),
        InlineKeyboardButton(f"{page}/{max_page}", callback_data="empty"),
        InlineKeyboardButton("➡", callback_data=article_data.new("right", max_page, page + 1, query)))
