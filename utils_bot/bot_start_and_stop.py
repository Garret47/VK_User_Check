from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from assist_func import json_methods
from bot_config import bot, config

FileNameCommands = "./data/commands.json"
FileNameMessageAdmins = './data/utils_message.json'
dict_commands = json_methods.read_file_json(FileNameCommands)
dict_message_admins = json_methods.read_file_json(FileNameMessageAdmins)


async def set_commands(bot: Bot):
    commands = []
    for i in dict_commands:
        commands.append(BotCommand(command=i, description=dict_commands[i]))
    await bot.set_my_commands(commands=commands)


async def send_message_admins(bot: Bot, message: list):
    for admin_id in config.ADMINS:
        try:
            await bot.send_message(admin_id, text=message[0])
            await bot.send_sticker(admin_id, sticker=message[1])
        except Exception as e:
            print(e)


async def start_bot(bot: Bot):
    await set_commands(bot)
    await send_message_admins(bot, dict_message_admins['start_bot'])


async def stop_bot(bot):
    await send_message_admins(bot, dict_message_admins['stop_bot'])