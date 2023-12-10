import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import router
from recognize import recognize_audio
import db.db as db


async def start_bot():
    global bot
    for id in db.admins_id():
        await bot.send_message(id, "Запуск бота Спич")


async def stop_bot():
    global bot
    for id in db.admins_id():
        await bot.send_message(id, "Спич завершил свою работу")

async def main():
    global bot
    bot = Bot(token=config["TELEGRAM"]["BOT_TOKEN"], parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="py_log.log", format="%(asctime)s %(levelname)s %(message)s")
    db.check_db()
    asyncio.run(main())