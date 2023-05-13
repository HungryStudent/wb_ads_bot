from aiogram.utils import executor
from create_bot import dp
from handlers import __init__
from middlewares.check_sub import CheckSubMiddleware

from utils import db


async def on_startup(_):
    db.start()


if __name__ == "__main__":
    dp.middleware.setup(CheckSubMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
