import asyncio

from aiogram import Bot, Router, types
from aiogram.enums import ChatAction
from aiogram.types import BusinessConnection
from aiogram.utils.chat_action import ChatActionSender

from filters.message import AdminSaysChiin, OthersSaysChiin
from filters.prompts import CheckAdminHello
from utils.choicer import start_sticker
from utils.writer import write

router = Router()


@router.business_connection()
async def on_bc(bc: BusinessConnection):
    print("BC ID:", bc.id)

@router.message(CheckAdminHello())
async def start(message: types.Message, bot: Bot):
    assert message.from_user
    await message.react([types.ReactionTypeEmoji(emoji="👏")])

    async with ChatActionSender(
        bot=bot, chat_id=message.from_user.id, action=ChatAction.CHOOSE_STICKER
    ):
        await asyncio.sleep(1)
        await message.answer_sticker(await start_sticker())

    async with ChatActionSender(
        bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
    ):
        await asyncio.sleep(1)

        await write("Assalomu alaykum, qanday savollaringiz bor?", message)

    async with ChatActionSender(
        bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
    ):
        await asyncio.sleep(0.5)

        await write("Sizga qanday yordam berishim mumkin?", message)


@router.business_message(AdminSaysChiin())
async def bussines_start(message: types.Message, bot: Bot):
    await message.answer_sticker(await start_sticker())
    await write("こんいちわ, Javohir qanaqasiz!", message=message)


@router.business_message(OthersSaysChiin())
async def bussines_other_start(message: types.Message, bot: Bot):
    assert message.from_user
    await write(
        f"Assalomu alaykum {message.from_user.first_name}, qanday savollaringiz bor?",
        message=message,
    )
