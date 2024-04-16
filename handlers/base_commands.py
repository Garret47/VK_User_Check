from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from FsmMachine import state_machines
from data import work_json

router_command = Router()
start_message = work_json.dict_command['start_message']
help_message = work_json.dict_command['help_message']
search_message = work_json.dict_command['search_message']


@router_command.message(Command('start'))
async def command_start(message: types.Message):
    await message.answer(start_message)


@router_command.message(Command('help'))
async def command_help(message: types.Message):
    await message.answer(help_message)


@router_command.message(Command('search'))
async def command_search(message: types.Message, state: FSMContext):
    await message.answer(search_message)
    await state.set_state(state_machines.VkSearchMachine.NumberChoice)
