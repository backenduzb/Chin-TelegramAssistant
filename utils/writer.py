import asyncio

TAG_PATTERNS = [
    (r"\*\*", r"\*\*"),       
    (r"\*", r"\*"),           
    (r"`", r"`"),             
    (r"```", r"```"),         
]

async def write(text: str, message):
    msg = await message.answer("...")

    words = text.split(" ")
    message_text = ""
    skip_buffer = ""
    in_tag = None  

    i = 0
    while i < len(words):
        word = words[i]

        if in_tag is None:
            for start, end in TAG_PATTERNS:
                if word.startswith(start):
                    in_tag = end
                    skip_buffer += word + " "
                    break

            if in_tag:
                i += 1
                continue

            message_text += word + " "
            try:
                await msg.edit_text(message_text.strip())
                await asyncio.sleep(0.08)
            except Exception as e:
                print("WRITE ERROR:", e)
                break

        else:
            skip_buffer += word + " "

            if word.endswith(in_tag):
                message_text += skip_buffer
                try:
                    await msg.edit_text(message_text.strip())
                    await asyncio.sleep(0.08)
                except Exception as e:
                    print("WRITE ERROR:", e)
                    break

                skip_buffer = ""
                in_tag = None

        i += 1

    return msg
