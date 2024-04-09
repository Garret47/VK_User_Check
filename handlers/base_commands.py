from aiogram import Router, types
from aiogram.filters import Command
from data import work_json

router_command = Router()
start_message = work_json.start_message
help_message = work_json.help_message


@router_command.message(Command('start'))
async def command_start(message: types.Message):
    await message.answer(start_message)


@router_command.message(Command('help'))
async def command_help(message: types.Message):
    await message.answer(help_message)