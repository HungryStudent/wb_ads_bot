from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update, ChatMember
from aiogram.utils.exceptions import ChatNotFound

from keyboards import user as user_kb
from config import channel_id
from create_bot import bot


class CheckSubMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: Update, data: dict):
        if update.message:
            if update.message.text == "/start":
                return
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        else:
            return

        try:
            status: ChatMember = await bot.get_chat_member(channel_id, user_id)
            if status.status == "left":
                if update.callback_query:
                    await update.callback_query.answer("Необходимо вступить в канал")
                else:
                    await bot.send_message(user_id,
                                           "Бот доступен бесплатно для подписчиков канала AUTOMATE MP, чтобы начать пользоваться, подпишитесь на канал 👉 @automate_mp",
                                           reply_markup=user_kb.check_sub)

                raise CancelHandler()
        except ChatNotFound as e:
            print(e)
            return
