from aiogram import Router, types, Bot
from aiogram.enums import ChatAction
from aiogram.utils.chat_action import ChatActionSender

from utils.connector import get_request_data
from utils.writer import write

router = Router()


@router.message()
async def response_with_ai(message: types.Message, bot: Bot):
    await message.react([types.ReactionTypeEmoji(emoji="👌")])
    assert message.from_user
    async with ChatActionSender(
        bot=bot, chat_id=message.from_user.id, action=ChatAction.RECORD_VOICE
    ):
        ai_response = await get_request_data(str(message.text))
    await message.answer(ai_response)
    await write(text=ai_response, message=message)
