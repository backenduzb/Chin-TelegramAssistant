from aiogram import Router, types

from filters.message import AdminIsOffline
from keyboards.inline.buttons import bot_button
from utils.writer import write

router = Router()


@router.business_message(AdminIsOffline())
async def admin_offline(message: types.Message):
    msg = await write(
        "Assalomu alaykum uzur Javohir hozir online emas. Online bo'lishi bilan albatta habaringizni o'qiydi.",
        message,
    )
    await msg.edit_reply_markup(reply_markup=await bot_button())
