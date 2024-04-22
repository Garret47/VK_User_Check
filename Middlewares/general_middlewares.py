from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class GeneralOutputMiddleware(BaseMiddleware):
    def __init__(self):
        self.refuse_send_message = set()

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]):
        user = data['event_from_user']
        if user.id not in self.refuse_send_message:
            self.refuse_send_message.add(user.id)
            result = await handler(event, data)
            self.refuse_send_message.remove(user.id)
            return result
        else:
            return
