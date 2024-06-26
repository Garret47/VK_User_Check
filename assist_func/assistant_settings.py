from aiogram import types
from aiogram.fsm.context import FSMContext
from Databases import SingletonBd
from data import TABLE_NAME_SETTING, DEFAULT_SETTINGS


def str_query(tables_columns: list, settings: dict, table: str, id_bd: int):
    query = 'Insert into {0} ({1}) values({2}) on duplicate key update {3}'
    tmp_columns = f'{tables_columns[0][0]}'
    tmp_values = f'{str(id_bd)}'
    tmp_update = ''
    separator = ''
    for i in tables_columns[1:]:
        quotes = ''
        if 'varchar' in i[1]:
            quotes = '"'
        key = settings.get(i[0])
        if key is None or key == '':
            key = DEFAULT_SETTINGS[i[0]]
        tmp_columns += f', {i[0]}'
        tmp_values += f', {quotes}{key}{quotes}'
        tmp_update += f'{separator}{i[0]}={quotes}{key}{quotes}'
        separator = ', '
    return query.format(table, tmp_columns, tmp_values, tmp_update)


async def callback_mode_assistant(callback: types.CallbackQuery, state: FSMContext, flag: bool):
    await callback.answer()
    await state.update_data(mode=callback.data)
    await state.update_data(all=flag)


async def finally_settings(message: types.Message, state: FSMContext, answer: str, user_id: int):
    await message.answer(answer, reply_markup=types.ReplyKeyboardRemove())
    settings = await state.get_data()
    bd = SingletonBd()
    columns = (await bd.describe_table())[TABLE_NAME_SETTING]
    query = str_query(columns, settings, TABLE_NAME_SETTING, user_id)
    await bd.insert_bd(query)
    await state.clear()
