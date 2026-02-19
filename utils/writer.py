from utils.formatter import markdown_to_html
import asyncio

async def write(text: str, message):
    safe_text = markdown_to_html(text)

    if "<pre><code>" in safe_text:
        return await message.answer(
            safe_text,
            parse_mode="HTML"
        )

    msg = await message.answer("...")
    words = text.split()
    message_text = ""

    for word in words:
        message_text += word + " "
        try:
            await msg.edit_text(message_text.strip())
            await asyncio.sleep(0.09)
        except Exception:
            break

    return msg
