import asyncio
from aiogram.enums import ParseMode
from utils.formatter import has_code_block, to_html_codeblock


async def write(text: str, message):
    if has_code_block(text):
        safe_text = to_html_codeblock(text)
        return await message.answer(
            safe_text,
            parse_mode=ParseMode.HTML
        )

    msg = await message.answer("...")
    words = text.split()
    message_text = ""

    for word in words:
        message_text += word + " "
        try:
            await msg.edit_text(message_text.strip())
            await asyncio.sleep(0.05)
        except Exception:
            break

    return msg
