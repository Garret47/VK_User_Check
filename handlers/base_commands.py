from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from FsmMachine import state_machines
from assist_func import json_methods

router_command = Router()
FileNameCommand = './data/command_message.json'
dict_command = json_methods.read_file_json(FileNameCommand)


@router_command.message(Command('start'))
async def command_start(message: types.Message):
    await message.answer(dict_command['start_message'])


@router_command.message(Command('help'))
async def command_help(message: types.Message):
    await message.answer(dict_command['help_message'])


@router_command.message(Command('search'))
async def command_search(message: types.Message, state: FSMContext):
    await message.answer(dict_command['search_message'])
    await state.set_state(state_machines.VkSearchMachine.NumberChoice)
