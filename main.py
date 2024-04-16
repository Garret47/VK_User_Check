import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import config
from handlers import base_commands
from aiogram.enums import ParseMode


async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(base_commands.router_command)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
