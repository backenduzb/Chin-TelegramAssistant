import asyncio

from aiogram import Bot, F, Router, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from methods.poststory import post_story
from states.admin import AdminState
from utils.writer import write

router = Router()


@router.message(F.video)
async def story_from_video(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()
    await message.react([types.ReactionTypeEmoji(emoji="👍")])
    assert message.from_user is not None
    assert message.video is not None
    async with ChatActionSender(
        bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
    ):
        await write(
            message=message,
            text="Captionlaringiz tog'rimi men upload qilaveraymi? Nima deysiz?",
        )
        await state.set_data(
            {"file_id": message.video.file_id, "caption": message.caption}
        )
        await state.set_state(AdminState.waiting_admin_response)


@router.message(AdminState.waiting_admin_response)
async def check_and_upload(message: types.Message, state: FSMContext, bot: Bot):
    text = str(message.text).lower()
    assert message.from_user is not None

    if "ha" in text or "upload qil" in text or "albatta" in text:
        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.CHOOSE_STICKER
        ):
            await asyncio.sleep(1)
            await message.answer_sticker(
                "CAACAgIAAxkBAAEaNiJpbkVKaw7UU2myc_t2SheNH7XP6AACizoAAqc-8EgQE5oIYjt6EDgE"
            )

        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
        ):
            await message.react([types.ReactionTypeEmoji(emoji="👌")])
            await write(message=message, text="Unaqada storyingizni upload qilayapman.")

        data = await state.get_data()
        file_id = data.get("file_id")
        caption = data.get("caption")
        if len(str(caption)) > 200:
            async with ChatActionSender(
                bot=bot, chat_id=message.chat.id, action=ChatAction.TYPING
            ):
                await write(
                    text="Sizning captioningiz telegramni limitidan ko'roq ekan 😅",
                    message=message,
                )
                await write(
                    text="Iltimos qisqaroq caption yozibberaolasizmi?", message=message
                )
                await state.set_state(AdminState.waiting_new_caption_response)

                return
        async with ChatActionSender(
            bot=bot, chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO
        ):
            await post_story(
                caption=caption or "Posted with @python_de_bot",
                video_file_id=file_id or "",
                message=message,
                life_time=86400,
            )

            await message.react([types.ReactionTypeEmoji(emoji="🔥")])
        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
        ):
            await write(message=message, text="Storyingini upload qildim")

    elif "yo'q" in text or "kerak emas" in text or "emas" in text:
        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.CHOOSE_STICKER
        ):
            await message.react([types.ReactionTypeEmoji(emoji="😢")])
            await message.answer_sticker(
                "CAACAgIAAxkBAAEaNiRpbkWQ3KJTPq99JqU0TsC0B8M3VQAC3D0AArc_8EhpmZXV6BW7-TgE"
            )

            await write(text="Bo'lmasa caption almashtirasizmi?", message=message)
            await state.set_state(AdminState.waiting_new_caption_response)
            return


@router.message(AdminState.waiting_new_caption_response)
async def get_caption(message: types.Message, state: FSMContext, bot: Bot):
    text = message.text

    if text in ["ha", "bor", "hop", "ok"]:
        async with ChatActionSender(
            bot=bot, chat_id=message.chat.id, action=ChatAction.TYPING
        ):
            await write(
                text="Aha unaqada captionni menga yozib yuboring", message=message
            )
            await state.set_state(AdminState.waiting_new_caption)
    else:
        assert message.from_user is not None
        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.CHOOSE_STICKER
        ):
            await message.react([types.ReactionTypeEmoji(emoji="😢")])
            await message.answer_sticker(
                "CAACAgIAAxkBAAEaNiRpbkWQ3KJTPq99JqU0TsC0B8M3VQAC3D0AArc_8EhpmZXV6BW7-TgE"
            )

            await write(text="Mayli unaqada upload qilmayman", message=message)
            await state.clear()
            return


@router.message(AdminState.waiting_new_caption)
async def check_caption(message: types.Message, bot: Bot, state: FSMContext):
    caption = message.text

    if len(str(caption)) > 200:
        await write(
            text=f"Bu captioningiz ham telegramni limitdan ko'proqda. Yana {200 - len(str(caption))} ta belgini olib tashlasangiz bo'ldi.",
            message=message,
        )
        await state.set_state(AdminState.waiting_new_caption)
        return
    else:
        async with ChatActionSender(
            bot=bot, chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO
        ):
            data = await state.get_data()
            file_id = data.get("file_id")
            await post_story(
                caption=caption or "Posted with @python_de_bot",
                video_file_id=file_id or "",
                message=message,
                life_time=86400,
            )

            await message.react(reaction=[types.ReactionTypeEmoji(emoji="🔥")])
