from typing import Any, Union, Dict
from aiogram import types
from FsmMachine import state_machines
import re
from aiogram.filters import BaseFilter


class FilterPermittedMessage(BaseFilter):
    def __init__(self, permitted_values: dict):
        self.permitted_values = permitted_values

    async def __call__(self, message: types.Message, *args, **kwargs):
        refactoring_mess = (re.sub(r'[^a-z@\._ ]', '', message.text)).split()
        len_message = len(set(refactoring_mess + list(self.permitted_values.keys())))
        if len_message != len(self.permitted_values.keys()) or refactoring_mess == []:
            return False
        else:
            return {'refactoring_message': ', '.join(list(set(refactoring_mess)))}
