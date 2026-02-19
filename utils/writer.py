import asyncio
import html
import re

HTML_PATTERN = re.compile(r"(<pre><code>.*?</code></pre>|<code>.*?</code>)", re.DOTALL)


def markdown_to_html(text: str) -> str:
    code_blocks = []
    inline_blocks = []

    def extract_block(match):
        code_blocks.append(match.group(1))
        return f"__BLOCK_{len(code_blocks) - 1}__"

    text = re.sub(r"```(?:\w+)?\n?(.*?)```", extract_block, text, flags=re.DOTALL)

    def extract_inline(match):
        inline_blocks.append(match.group(1))
        return f"__INLINE_{len(inline_blocks) - 1}__"

    text = re.sub(r"`(.*?)`", extract_inline, text)

    text = html.escape(text, quote=False)

    for i, code in enumerate(code_blocks):
        safe_code = html.escape(code, quote=False)
        text = text.replace(f"__BLOCK_{i}__", f"<pre><code>{safe_code}</code></pre>")

    for i, code in enumerate(inline_blocks):
        safe_code = html.escape(code, quote=False)
        text = text.replace(f"__INLINE_{i}__", f"<code>{safe_code}</code>")

    return text


async def write(text: str, message):
    text = markdown_to_html(text)
    parts = HTML_PATTERN.split(text)

    msg = await message.answer("...")
    final_text = ""

    for part in parts:
        if not part:
            continue

        if HTML_PATTERN.fullmatch(part):
            final_text += part
            try:
                await msg.edit_text(final_text, parse_mode="HTML")
                await asyncio.sleep(0.2)
            except Exception as e:
                print("WRITE ERROR:", e)
                break
        else:
            words = part.split(" ")
            for word in words:
                final_text += word + " "
                try:
                    await msg.edit_text(final_text.strip(), parse_mode="HTML")
                    await asyncio.sleep(0.2)
                except Exception as e:
                    print("WRITE ERROR:", e)
                    break

    return msg
