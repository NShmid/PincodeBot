from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.database.db import sellers


class IsSeller(BaseFilter):
    async def __call__(self, message: Message):
        return message.from_user.id in sellers