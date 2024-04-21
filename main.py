import asyncio
from aiogram import Bot, Dispatcher
from handlers import base_commands, settings_states_process, search_vk_keywords
from bot_config import config, dp, bot
from Databases import SingletonBd
from data import TABLES_DATABASE

bot: Bot
dp: Dispatcher


async def main():
    bd = SingletonBd(TABLES_DATABASE)
    await bd.bd_connect(host=config.HOST, user=config.USER_BD, password=config.PASSWORD_BD,
                        port=config.PORT, database=config.DATABASE)
    dp.include_routers(base_commands.router_command, settings_states_process.router_state_setting,
                       search_vk_keywords.router_search)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
