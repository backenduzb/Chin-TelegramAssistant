from aiogram.filters import BaseFilter
from aiogram.types import Message
from config.responses import ADMIN_SAYS_HELLO

class CheckAdminHello(BaseFilter):
    async def __call__(self, message: Message):
        assert message.text
        return message.text.lower() in ADMIN_SAYS_HELLO

class CheckAdminHelp(BaseFilter):
    async def __call__(self, message: Message):
        assert message.text
        return 'Chiin'.lower() in message.text.lower() and ('bilibber' in message.text.lower() or 'yozibber' in message.text.lower() and 'ayt' in message.text.lower() and 'aytibber' in message.text.lower())