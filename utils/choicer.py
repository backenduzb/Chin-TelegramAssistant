from random import choice
from config.settings import START_STICKERS

async def start_sticker() -> str:
    return choice(START_STICKERS)