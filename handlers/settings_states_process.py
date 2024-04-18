from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FsmMachine import state_machines
from filters import filters_state
from keyboards import state_settings_keyboards
from assist_func import json_methods, assistant_settings

router_state_setting = Router()
FileNameStateSettings = './data/state_settings_message.json'
dict_settings_message = json_methods.read_file_json(FileNameStateSettings)


async def change_state_on_people(message: types.Message, state: FSMContext, keyboard: types.InlineKeyboardMarkup):
    flag = (await state.get_data())['all']
    if flag:
        await message.answer(dict_settings_message['message_callback_people'], reply_markup=keyboard)
        await state.set_state(state_machines.VkSettingMachine.People)
    else:
        await assistant_settings.finally_settings(message, state, dict_settings_message['finally'])


@router_state_setting.message(F.text == state_settings_keyboards.text_keyboards['cancel_state'],
                              ~StateFilter(default_state))
async def cancel_settings_state(message: types.Message, state: FSMContext):
    await message.answer(text=state_settings_keyboards.text_keyboards['cancel_state'],
                         reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@router_state_setting.message(F.text.regexp(r"^(-?\d+)$"), state_machines.VkSettingMachine.NumberChoice)
async def state_number_choice(message: types.Message, state: FSMContext):
    digits = int(message.text)
    if (digits >= 1) and (digits <= 1000):
        kb_inline = state_settings_keyboards.kb_inline_state_mode
        await message.answer(dict_settings_message['message_number'], reply_markup=kb_inline)
        await state.update_data(digits=digits)
        await state.set_state(state_machines.VkSettingMachine.SettingModeChoice)
    else:
        await message.answer(dict_settings_message['message_error_number'].format(str(digits)))


@router_state_setting.message(state_machines.VkSettingMachine.NumberChoice)
async def error_state_number_choice(message: types.Message):
    await message.answer(dict_settings_message['message_not_number'])


@router_state_setting.callback_query(state_machines.VkSettingMachine.SettingModeChoice, F.data == 'communities')
async def state_choice_communities(callback: types.CallbackQuery, state: FSMContext):
    kb_inline = state_settings_keyboards.kb_inline_state_setting_value
    await callback.message.answer(dict_settings_message['message_callback_communities'], reply_markup=kb_inline)
    await assistant_settings.callback_mode_assistant(callback, state, False)
    await state.set_state(state_machines.VkSettingMachine.Communities)


@router_state_setting.callback_query(state_machines.VkSettingMachine.SettingModeChoice, F.data == 'people')
async def state_choice_people(callback: types.CallbackQuery, state: FSMContext):
    kb_inline = state_settings_keyboards.kb_inline_state_setting_value
    await callback.message.answer(dict_settings_message['message_callback_people'], reply_markup=kb_inline)
    await assistant_settings.callback_mode_assistant(callback, state, False)
    await state.set_state(state_machines.VkSettingMachine.People)


@router_state_setting.callback_query(state_machines.VkSettingMachine.SettingModeChoice, F.data == 'all')
async def state_choice_all(callback: types.CallbackQuery, state: FSMContext):
    kb_inline = state_settings_keyboards.kb_inline_state_setting_value
    await callback.message.answer(dict_settings_message['message_callback_communities'], reply_markup=kb_inline)
    await assistant_settings.callback_mode_assistant(callback, state, True)
    await state.set_state(state_machines.VkSettingMachine.Communities)


@router_state_setting.message(state_machines.VkSettingMachine.Communities, F.text)
async def state_communities(message: types.Message, state: FSMContext):
    kb_inline = state_settings_keyboards.kb_inline_state_setting_value
    await state.update_data(communities=message.text)
    await change_state_on_people(message, state, kb_inline)


@router_state_setting.message(state_machines.VkSettingMachine.People, F.text)
async def state_people(message: types.Message, state: FSMContext):
    await state.update_data(people=message.text)
    await assistant_settings.finally_settings(message, state, dict_settings_message['finally'])


@router_state_setting.callback_query(state_machines.VkSettingMachine.Communities, F.data == 'default')
async def callback_state_communities(callback: types.CallbackQuery, state: FSMContext):
    kb_inline = state_settings_keyboards.kb_inline_state_setting_value
    await state.update_data(communities='')
    await change_state_on_people(callback.message, state, kb_inline)
    await callback.answer()


@router_state_setting.callback_query(state_machines.VkSettingMachine.People, F.data == 'default')
async def callback_state_people(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(people='')
    await assistant_settings.finally_settings(callback.message, state, dict_settings_message['finally'])
    await callback.answer()


@router_state_setting.callback_query()
async def callback_tap(callback: types.CallbackQuery):
    await callback.answer()
