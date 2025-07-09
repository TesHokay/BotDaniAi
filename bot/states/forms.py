from aiogram.fsm.state import StatesGroup, State

class RequestForm(StatesGroup):
    service = State()
    description = State()
