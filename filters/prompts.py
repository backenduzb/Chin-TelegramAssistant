from aiogram.filters import BaseFilter
from aiogram.types import Message
from config.responses import ADMIN_SAYS_HELLO

class CheckAdminHello(BaseFilter):
    async def __call__(self, message: Message):
        assert message.text
        return message.text.lower() in ADMIN_SAYS_HELLO