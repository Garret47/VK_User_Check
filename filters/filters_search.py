from aiogram.filters import BaseFilter
from assist_func import assistant_filter_file
from aiogram import types
from data import MAX_BYTE_TELEGRAM


class FilterLoadFile(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs):
        if message.document.file_size > MAX_BYTE_TELEGRAM:
            return False
        return True


class FilterFileToDataframe(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs):
        url = await assistant_filter_file.create_url(message)
        response_bytes = await assistant_filter_file.request_telegram_file(url, message.document.file_size)
        if response_bytes is None:
            return False
        settings = await assistant_filter_file.read_settings_database(message.from_user.id)
        df = await assistant_filter_file.create_dataframe(settings, response_bytes)
        if df is None:
            return False
        return {'df': df, 'settings': settings}
