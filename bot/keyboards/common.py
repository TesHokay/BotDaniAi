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

finish_services_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Готово")],
    [KeyboardButton(text="Отмена")],
], resize_keyboard=True)

back_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Назад")]
], resize_keyboard=True)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Список заявок")],
        [KeyboardButton(text="Отправка рассылки")],
        [KeyboardButton(text="Редактировать услуги")],
        [KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
)


def requests_kb(requests):
    rows = [[InlineKeyboardButton(text=f"#{r[0]} | {r[2]} | {r[3]}", callback_data=f"req_{r[0]}")]
            for r in requests]
    rows.append([InlineKeyboardButton(text="Назад", callback_data="admin_back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def request_detail_kb(req_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data=f"del_{req_id}")],
            [InlineKeyboardButton(text="Назад", callback_data="back_requests")],
        ]
    )


def confirm_delete_kb(req_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data=f"delc_{req_id}")],
            [InlineKeyboardButton(text="Нет", callback_data=f"req_{req_id}")],
        ]
    )
