import io

from aiogram import Router, types, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.utils.chat_action import ChatActionSender
from filters import filters_search
from assist_func import json_methods, run_vk_search, create_file
import pandas as pd

router_search = Router()
FileNameSearchProcess = './data/search_message.json'
dict_search = json_methods.read_file_json(FileNameSearchProcess)


@router_search.message(F.document, StateFilter(default_state), filters_search.FilterLoadFile(),
                       filters_search.FilterFileToDataframe())
async def load_file(message: types.Message, df: pd.DataFrame, settings: dict):
    await message.answer(dict_search['message_successful_file_waiting'])
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        df_custom = await run_vk_search(df, settings, message)
    async with ChatActionSender.upload_document(bot=message.bot, chat_id=message.chat.id):
        files_bytes = await create_file(df_custom)
        for i in files_bytes:
            if files_bytes[i] is not None:
                file = types.BufferedInputFile(files_bytes[i].getvalue(), filename=f'{i}.xlsx')
                await message.bot.send_document(chat_id=message.chat.id, document=file)
            else:
                await message.answer(dict_search['message_error_send_file_too_big'])


@router_search.message(F.document, StateFilter(default_state), filters_search.FilterLoadFile())
async def file_error(message: types.Message):
    await message.answer(dict_search['message_error_excel_file'])


@router_search.message(F.document, StateFilter(default_state))
async def load_file(message: types.Message):
    await message.answer(dict_search['message_too_big_file'])
