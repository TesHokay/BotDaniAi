from aiogram.fsm.state import StatesGroup, State

class RequestForm(StatesGroup):
    service = State()
    description = State()
    contact = State()


class ServiceForm(StatesGroup):
    """Legacy form for adding separate service entries."""
    file = State()
    caption = State()


class ServicesMessageForm(StatesGroup):
    """State for receiving a single message describing all services."""
    content = State()


class NewsForm(StatesGroup):    content = State()