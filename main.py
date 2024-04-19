import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers import base_commands, settings_states_process
from aiogram.enums import ParseMode
from config import config
from Databases import SingletonBd

tables_name = ['bot_settings']


async def main():
    bd = SingletonBd(tables_name)
    await bd.bd_connect(host=config.HOST, user=config.USER_BD, password=config.PASSWORD_BD,
                        port=config.PORT, database=config.DATABASE)
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(base_commands.router_command, settings_states_process.router_state_setting)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
