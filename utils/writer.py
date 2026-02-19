import asyncio

async def write(text: str, message):
    msg = await message.answer("...")
    
    words = text.split()
    message_text = ""
    
    for word in words:
        message_text += word + " "
        
        try:
            await msg.edit_text(
                text=message_text.strip()
            )
            await asyncio.sleep(0.15)
        
        except Exception as e:
            print("WRITE ERROR:", e)
            break

    return msg