from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FsmMachine import state_machines
from keyboards import state_search_keyboards
from assist_func import json_methods

router_command = Router()
FileNameCommand = './data/command_message.json'
dict_command = json_methods.read_file_json(FileNameCommand)


@router_command.message(Command('start'), StateFilter(default_state))
async def command_start(message: types.Message):
    await message.answer(dict_command['start_message'])


@router_command.message(Command('help'), StateFilter(default_state))
async def command_help(message: types.Message):
    await message.answer(dict_command['help_message'])


@router_command.message(Command('search'), StateFilter(default_state))
async def command_search(message: types.Message, state: FSMContext):
    await message.answer(dict_command['search_message'], reply_markup=state_search_keyboards.kb_reply_state_search)
    await state.set_state(state_machines.VkSearchMachine.NumberChoice)
