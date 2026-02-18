from aiogram.fsm.context import FSMContext
from methods.poststory import post_story
from config.settings import BS_ID
from utils.imports import *
from states.admin import AdminState

router = Router()

@router.message(F.video)
async def story_from_video(message: types.Message, state: FSMContext,bot: Bot):
    await state.clear()
    await message.react([types.ReactionTypeEmoji(emoji="👍")])
    async with ChatActionSender(
        bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
    ):
        await write(
            message=message,
            text="Captionlaringiz tog'rimi men upload qilaveraymi? Nima deysiz?"
        )
        await state.set_data({"file_id": message.video.file_id, "caption":message.caption})
        await state.set_state(AdminState.waiting_admin_response)
 
@router.message(AdminState.waiting_admin_response)
async def check_and_upload( message: types.Message, state: FSMContext, bot: Bot):
    text = str(message.text).lower()
    if "ha" in text or "upload qil" in text or "albatta" in text:
        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.CHOOSE_STICKER
        ):
            await asyncio.sleep(1)
            await message.answer_sticker("CAACAgIAAxkBAAEaNiJpbkVKaw7UU2myc_t2SheNH7XP6AACizoAAqc-8EgQE5oIYjt6EDgE")

        
        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
        ):
            await message.react([types.ReactionTypeEmoji(emoji="👌")])
            await write(message=message, text="Unaqada storyingizni upload qilayapman.")
            
        data = await state.get_data()
        file_id = data.get("file_id")
        caption = data.get("caption")
          
        async with ChatActionSender(
            bot=bot,chat_id=message.chat.id, action=ChatAction.UPLOAD_VIDEO
                    ):
            await post_story(
                caption=caption or "Posted with @python_de_bot",
                video_file_id=file_id or "",
                message=message,
                life_time=86400
            )
            
            await message.react([types.ReactionTypeEmoji(emoji='🔥')])
        async with ChatActionSender(
                bot=bot, chat_id=message.from_user.id, action=ChatAction.TYPING
        ):
                await write(message=message, text="Storyingini upload qildim")

    elif "yo'q" in text or "kerak emas" in text or "emas" in text:
        async with ChatActionSender(
            bot=bot, chat_id=message.from_user.id, action=ChatAction.CHOOSE_STICKER
        ):
            await message.react([types.ReactionTypeEmoji(emoji="😢")])
            await message.answer_sticker("CAACAgIAAxkBAAEaNiRpbkWQ3KJTPq99JqU0TsC0B8M3VQAC3D0AArc_8EhpmZXV6BW7-TgE")
            await state.clear()
            return