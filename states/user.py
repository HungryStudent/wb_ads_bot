from aiogram.dispatcher.filters.state import StatesGroup, State


class Search(StatesGroup):
    query = State()


class Card(StatesGroup):
    article = State()
