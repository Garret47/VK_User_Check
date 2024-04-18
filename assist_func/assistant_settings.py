from aiogram import types
from aiogram.fsm.context import FSMContext


async def callback_mode_assistant(callback: types.CallbackQuery, state: FSMContext, flag: bool):
    await callback.answer()
    await state.update_data(mode=callback.data)
    await state.update_data(all=flag)


async def finally_settings(message: types.Message, state: FSMContext, answer: str):
    await message.answer(answer, reply_markup=types.ReplyKeyboardRemove())
    print(await state.get_data())
    await state.clear()
