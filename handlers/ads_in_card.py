from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from states import user as states
import keyboards.user as user_kb
from create_bot import dp
from utils import db, wb


@dp.callback_query_handler(text="ads_in_card")
async def enter_article(call: CallbackQuery):
    await call.message.edit_text("Напишите артикул товара, например: 81728391")
    await states.Card.article.set()


@dp.message_handler(state=states.Card.article)
async def get_article(message: Message, state: FSMContext):
    msg = await message.answer("Загрузка...")
    user = db.get_user(message.from_user.id)
    data = wb.get_card(message.text, 1, user["city_code"])
    if data is None:
        await message.answer(
            f'Ставки по рекламным кампаниям по артикулу: "{message.text}":\n\nРекламных кампаний не найдено.',
            reply_markup=user_kb.back_to_menu)
    else:
        await message.answer(data["msg_text"],
                             reply_markup=user_kb.get_article(data["products_count"], 1, message.text))
    await msg.delete()
    await state.finish()


@dp.callback_query_handler(user_kb.article_data.filter())
async def flip_article(call: CallbackQuery, callback_data: dict):
    if int(callback_data["page"]) == 0:
        await call.answer("Вы на первой странице")
        return
    elif int(callback_data["page"]) == int(callback_data["max_page"]) + 1:
        await call.answer("Вы на последней странице")
        return
    user = db.get_user(call.from_user.id)
    data = wb.get_card(callback_data["query"], int(callback_data["page"]), user["city_code"])
    if data is None:
        await call.message.edit_text(
            f'Ставки по рекламным кампаниям по запросу: "{callback_data["query"]}":\n\nРекламных кампаний не найдено.',
            reply_markup=user_kb.back_to_menu)
    else:
        try:
            await call.message.edit_text(data["msg_text"],
                                         reply_markup=user_kb.get_article(int(data["products_count"]),
                                                                          int(callback_data["page"]),
                                                                          callback_data["query"]))
        except MessageNotModified:
            await call.answer()