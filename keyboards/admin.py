from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

def get_prompt(prompt_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Изменить название", callback_data=f"change:name:{prompt_id}"),
        InlineKeyboardButton("Изменить промпт", callback_data=f"change:content:{prompt_id}"),
        InlineKeyboardButton("Удалить промпт", callback_data=f"delete_prompt:{prompt_id}"))


def get_delete(prompt_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Да, удалить", callback_data=delete_prompt_callback.new("approve", prompt_id)),
        InlineKeyboardButton("Нет, не удалять", callback_data=delete_prompt_callback.new("cancel", prompt_id)))
