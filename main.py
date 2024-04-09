import asyncio
from aiogram import Bot, Dispatcher, types
from config import config


async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
