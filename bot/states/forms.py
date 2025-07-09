from aiogram.fsm.state import StatesGroup, State

class RequestForm(StatesGroup):
    service = State()
    description = State()
    contact = State()


class ServiceForm(StatesGroup):
    name = State()


class NewsForm(StatesGroup):
    text = State()
