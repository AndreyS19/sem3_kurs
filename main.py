import asyncio
import logging
import sys
from app.handlers import dp
from aiogram import Bot, Dispatcher

from app.data_processing import  data_reset_closing, get_var


async def main():
    bot = Bot(get_var("token"))
    disp = Dispatcher()
    disp.include_router(dp)
    try:
        await disp.start_polling(bot)
    except asyncio.exceptions.CancelledError:
        data_reset_closing()
        await bot.session.close()
    finally:
        data_reset_closing()
        await bot.session.close()
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
