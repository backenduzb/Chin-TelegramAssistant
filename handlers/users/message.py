from aiogram import  Router, types

from utils.writer import write
from utils.connector import get_request_data

router = Router()

@router.message()
async def response_with_ai(message: types.Message):
    ai_response = await get_request_data(str(message.text))
    
    await write(
        text=ai_response,
        message=message
    )