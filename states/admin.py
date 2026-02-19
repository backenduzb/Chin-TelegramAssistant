from aiogram.fsm.state import State, StatesGroup

class AdminState(StatesGroup):
    waiting_admin_response = State()
    waiting_new_caption_response = State()
    waiting_new_caption = State()