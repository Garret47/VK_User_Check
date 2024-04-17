from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from FsmMachine import state_machines
from filters import filters_state_load_file
from keyboards import state_search_keyboards
from assist_func import json_methods

router_state_search = Router()
FileNameStateSearch = './data/state_search_message.json'
dict_search_message = json_methods.read_file_json(FileNameStateSearch)


@router_state_search.message(F.text.regexp(r"^(-?\d+)$"), state_machines.VkSearchMachine.NumberChoice)
async def state_number_choice(message: types.Message, state: FSMContext):
    digits = int(message.text)
    if (digits >= 1) and (digits <= 1000):
        kb_inline = state_search_keyboards.kb_inline_state_search
        await message.answer(dict_search_message['message_number'], reply_markup=kb_inline)
        await state.set_state(state_machines.VkSearchMachine.SearchModeChoice)
    else:
        await message.answer(dict_search_message['message_error_number'].format(str(digits)))


@router_state_search.message(state_machines.VkSearchMachine.NumberChoice)
async def error_state_number_choice(message: types.Message):
    await message.answer(dict_search_message['message_not_number'])


@router_state_search.callback_query(state_machines.VkSearchMachine.SearchModeChoice, F.data.in_({'communities',
                                                                                                 'people', 'all'}))
async def state_choice_mode_search(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(dict_search_message['message_callback_answer'])
    await callback.answer()
    await
    await state.set_state(state_machines.VkSearchMachine.LoadFile)


@router_state_search.callback_query(F.data.in_({'communities', 'people', 'all'}))
async def state_not_choice_mode_search(callback: types.CallbackQuery):
    await callback.answer()


@router_state_search.message(state_machines.VkSearchMachine.LoadFile, F.document,
                             filters_state_load_file.FilterLoadFile())
async def state_load_file(message: types.Message):
    await message.answer(dict_search_message['message_load_file'])


@router_state_search.message(state_machines.VkSearchMachine.LoadFile, F.document)
async def state_big_load_file(message: types.Message):
    await message.answer(dict_search_message['message_too_big_file'])


@router_state_search.message(state_machines.VkSearchMachine.LoadFile, F.content_type.in_({types.ContentType.PHOTO,
                                                                                          types.ContentType.VIDEO}))
async def state_error_text_file(message: types.Message):
    await message.answer(dict_search_message['message_not_text_file'])


@router_state_search.message(state_machines.VkSearchMachine.LoadFile, ~F.content_type.in_({types.ContentType.PHOTO,
                                                                                           types.ContentType.VIDEO,
                                                                                           types.ContentType.DOCUMENT}))
async def state_error_file(message: types.Message):
    await message.answer(dict_search_message['message_not_file'])
