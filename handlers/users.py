from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatMember

import keyboards.user as user_kb
from config import channel_id
from create_bot import dp
from utils import db


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: Message, state: FSMContext):
    await state.finish()

    user = db.get_user(message.from_user.id)
    if user is None:
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)

    status: ChatMember = await message.bot.get_chat_member(channel_id, message.from_user.id)
    if status.status == "left":
        await message.bot.send_message(message.from_user.id,
                                       "Бот доступен бесплатно для подписчиков канала AUTOMATE MP, чтобы начать пользоваться, подпишитесь на канал 👉 @automate_mp",
                                       reply_markup=user_kb.check_sub)
        return

    await message.answer("""<b>Узнайте актуальные рекламные ставки ваших конкурентов на WB</b>

1️⃣ WB часто предлагает рекламу по высоким ставкам, но на самом деле, ставки для занятия этих мест гораздо ниже

2️⃣ Вы узнаете реальные ставки, которые на самом деле ниже на 50, 70, а иногда и 90%, чем те, что предлагает WB

3️⃣ Оптимизируйте расходы за счет оплаты по актуальным ставкам.

Ставки можно проверить в поиске WB или в карточке товара, нажмите соответствующую кнопку.

⚙ В настройках вы можете задать регион и пол аккаунта, с которого будет производится проверка. По умолчанию установлено: МСК, пол: Не указан
""", reply_markup=user_kb.menu)


@dp.message_handler(state="*", text="Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Ввод отменен", reply_markup=user_kb.menu)



