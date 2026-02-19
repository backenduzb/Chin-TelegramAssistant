import asyncio
import html
import re

HTML_TAGS = ["<b>", "</b>", "<i>", "</i>", "<code>", "</code>", "<pre>", "</pre>"]

HTML_PATTERN = re.compile(r"(<pre>.*?</pre>|<code>.*?</code>|<b>.*?</b>|<i>.*?</i>)", re.DOTALL)

async def write(text: str, message):
    parts = HTML_PATTERN.split(text)  

    msg = await message.answer("…")
    final_text = ""

    for part in parts:
        if not part:
            continue

        if any(tag in part for tag in HTML_TAGS):
            final_text += part
            try:
                await msg.edit_text(final_text, parse_mode="HTML")
                await asyncio.sleep(0.08)
            except Exception as e:
                print("WRITE ERROR:", e)
                break
        else:
            words = part.split(" ")
            for word in words:
                final_text += html.escape(word) + " "
                try:
                    await msg.edit_text(final_text.strip(), parse_mode="HTML")
                    await asyncio.sleep(0.07)
                except Exception as e:
                    print("WRITE ERROR:", e)
                    break

    return msg
