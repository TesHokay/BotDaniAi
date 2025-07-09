from aiogram.fsm.state import StatesGroup, State

class RequestForm(StatesGroup):
    service = State()
    description = State()
    contact = State()


class ServiceForm(StatesGroup):
    file = State()
    caption = State()


class NewsForm(StatesGroup):
    content = State()