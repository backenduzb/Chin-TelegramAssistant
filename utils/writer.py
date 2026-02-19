import asyncio
import re
from utils.formatter import markdown_to_html
from aiogram.enums import ParseMode

async def write(text: str, message):
    safe_text = markdown_to_html(text)
    
    pattern = re.compile(r"(<pre><code>.*?</code></pre>|<code>.*?</code>)", re.DOTALL)
    parts = pattern.split(safe_text)  

    msg = await message.answer("")

    for part in parts:
        if not part:
            continue
        if part.startswith("<pre><code>") or part.startswith("<code>"):
            await msg.edit_text(part, parse_mode=ParseMode.HTML)
            await asyncio.sleep(0.07)
        else:
            words = part.split()
            message_text = ""
            for word in words:
                message_text += word + " "
                try:
                    await msg.edit_text(message_text.strip(), parse_mode=ParseMode.HTML)
                    await asyncio.sleep(0.07)
                except Exception:
                    break

    return msg
