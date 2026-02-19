import asyncio
import html
import re

HTML_TAGS = ["<b>", "</b>", "<i>", "</i>", "<code>", "</code>", "<pre>", "</pre>"]
HTML_PATTERN = re.compile(r"(<pre>.*?</pre>|<code>.*?</code>|<b>.*?</b>|<i>.*?</i>)", re.DOTALL)

def markdown_to_html(text: str) -> str:
    text = re.sub(r"```python(.*?)```", r"<pre><code>\1</code></pre>", text, flags=re.DOTALL)
    text = re.sub(r"`python(.*?)`", r"<code>\1</code>", text)
    text = html.escape(text, quote=False)
    text = text.replace("&lt;pre&gt;", "<pre>").replace("&lt;/pre&gt;", "</pre>")
    text = text.replace("&lt;code&gt;", "<code>").replace("&lt;/code&gt;", "</code>")
    return text

async def write(text: str, message):
    text = markdown_to_html(text)

    parts = HTML_PATTERN.split(text)  

    msg = await message.answer("...")
    final_text = ""

    for part in parts:
        if not part:
            continue

        if any(tag in part for tag in HTML_TAGS):
            final_text += part
            try:
                await msg.edit_text(final_text, parse_mode="HTML")
                await asyncio.sleep(0.1)
            except Exception as e:
                print("WRITE ERROR:", e)
                break
        else:
            words = part.split(" ")
            for word in words:
                final_text += word + " "
                try:
                    await msg.edit_text(final_text.strip(), parse_mode="HTML")
                    await asyncio.sleep(0.07)
                except Exception as e:
                    print("WRITE ERROR:", e)
                    break

    return msg
