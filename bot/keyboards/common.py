from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Заполнить анкету")],
        [KeyboardButton(text="Мои услуги")],
        [KeyboardButton(text="Написать напрямую DaniAi")],
    ],
    resize_keyboard=True,
)

cancel_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отмена")]
], resize_keyboard=True)

back_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Назад")]
], resize_keyboard=True)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Список заявок")],
        [KeyboardButton(text="Добавить пример работы")],
        [KeyboardButton(text="Добавить услугу")],
        [KeyboardButton(text="Рассылка новости")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)
