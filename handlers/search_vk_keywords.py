from aiogram import Router, types, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from filters import filters_search
from assist_func import json_methods
import pandas as pd

router_search = Router()
FileNameSearchProcess = './data/search_message.json'
dict_search = json_methods.read_file_json(FileNameSearchProcess)


@router_search.message(F.document, StateFilter(default_state), filters_search.FilterLoadFile(),
                       filters_search.FilterFileToDataframe())
async def load_file(message: types.Message, df: pd.DataFrame, settings: dict):
    print(df)
    print(settings)


@router_search.message(F.document, StateFilter(default_state), filters_search.FilterLoadFile())
async def file_error(message: types.Message):
    await message.answer(dict_search['message_error_excel_file'])


@router_search.message(F.document, StateFilter(default_state))
async def load_file(message: types.Message):
    await message.answer(dict_search['message_too_big_file'])
