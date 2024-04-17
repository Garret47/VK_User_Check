from typing import Any, Union, Dict
from aiogram import types
from FsmMachine import state_machines

from aiogram.filters import BaseFilter

CONST_MAX_SIZE_FILE = 20971520


class FilterLoadFile(BaseFilter):
    async def __call__(self, message: types.Message, **kwargs):
        if message.document.file_size <= CONST_MAX_SIZE_FILE:
            return True
        return False
