import aiohttp
from aiogram import types, Bot
from bot_config import config
import pandas as pd
import io
from data import STANDARD_URL_TELEGRAM, TIMEOUT_READ_FILE, TABLE_NAME_SETTING, DEFAULT_SETTINGS
from Databases import SingletonBd


async def create_url(message: types.Message):
    try:
        path = await message.bot.get_file(message.document.file_id)
        url = STANDARD_URL_TELEGRAM + config.BOT_TOKEN.get_secret_value() + '/' + path.file_path
        return url
    except TimeoutError:
        return


async def request_telegram_file(url: str, file_size: int):
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(url, timeout=TIMEOUT_READ_FILE)
            if response.status == 200:
                response_bytes = await response.content.readexactly(file_size)
                return response_bytes
            else:
                return
        except TimeoutError:
            return


async def read_settings_database(user_id):
    bd = SingletonBd()
    answer = await bd.select_bg(f'select * from {TABLE_NAME_SETTING} WHERE id={user_id}')
    default = DEFAULT_SETTINGS
    default['id'] = user_id
    if answer:
        settings = dict(zip(tuple(default.keys()), answer[0]))
    else:
        settings = default
    return settings


async def create_dataframe(settings: dict, response_bytes: bytes):
    try:
        f = io.BytesIO(response_bytes)
        df = pd.read_excel(f, usecols=['q', 'count'])
        if df.shape[0] > settings['count']:
            df = df[:settings['count']]
        return df
    except Exception as e:
        print(e)
        return
