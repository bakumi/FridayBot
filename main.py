import asyncio
import logging
from aiogram import Bot, Dispatcher

from app.handlers import router
from config import TOKEN
from app.admin import admin



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router, admin)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')