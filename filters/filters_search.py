from aiogram.filters import BaseFilter
from assist_func import assistant_filter_file
from aiogram import types
from data import MAX_BYTE_TELEGRAM
from aiogram.utils.chat_action import ChatActionSender


class FilterLoadFile(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs):
        if message.document.file_size > MAX_BYTE_TELEGRAM:
            return False
        return True


class FilterFileToDataframe(BaseFilter):
    async def __call__(self, message: types.Message, *args, **kwargs):
        async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
            url = await assistant_filter_file.create_url(message)
            if url is None:
                return False
            response_bytes = await assistant_filter_file.request_telegram_file(url, message.document.file_size)
            if response_bytes is None:
                return False
            settings = await assistant_filter_file.read_settings_database(message.from_user.id)
            df = await assistant_filter_file.create_dataframe(settings, response_bytes)
            if df is None or df.empty:
                return False
        df = df.drop_duplicates(subset=['q'], ignore_index=True)
        df.loc[df['count'] > 200, 'count'] = 200
        return {'df': df, 'settings': settings}
