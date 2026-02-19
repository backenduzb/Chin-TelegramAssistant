from aiogram import Bot, Router, types
from aiogram.enums import ChatAction
from aiogram.utils.chat_action import ChatActionSender

from filters.message import AdminIsOffline
from filters.prompts import CheckAdminHelp
from keyboards.inline.buttons import bot_button
from utils.connector import get_request_data
from utils.writer import write

router = Router()


@router.business_message(AdminIsOffline())
async def admin_offline(message: types.Message):
    msg = await write(
        "Assalomu alaykum uzur Javohir hozir online emas. Online bo'lishi bilan albatta habaringizni o'qiydi.\n\n Hohlasangiz men bilan suhbatlashishingiz mumkin. Dasturlash boyicha qiziqqan savolaringizga javobbera olaman.",
        message,
    )
    await msg.edit_reply_markup(reply_markup=await bot_button())


@router.business_message(CheckAdminHelp())
async def get_ai_response_for_admin(bot: Bot, message: types.Message):
    assert message.from_user
    async with ChatActionSender(
        bot=bot, chat_id=message.from_user.id, action=ChatAction.RECORD_VOICE
    ):
        ai_response = await get_request_data(str(message.text))
    await write(text=ai_response, message=message)
