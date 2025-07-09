from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.fsm.context import FSMContext
from ..keyboards.common import main_menu, cancel_kb, back_kb, admin_menu
from ..states.forms import RequestForm
from ..db.dao import Database
from ..config import settings

router = Router()

db = Database(settings.db_path)


async def send_services(msg: types.Message) -> bool:
    """Send stored services message to the user."""
    service_ids = db.get_service_messages()
    if not service_ids:
        return False
    ok = False
    for sid in service_ids:
        try:
            await msg.bot.copy_message(msg.chat.id, settings.admin_id, sid)
            ok = True
        except Exception:
            pass
    return ok

@router.message(CommandStart())
async def start(msg: types.Message):
    db.add_user(msg.from_user.id, msg.from_user.username or "")
    if msg.from_user.id == settings.admin_id:
        await msg.answer("Админ меню", reply_markup=admin_menu)
        return
    await send_services(msg)
    await msg.answer("Выберите опцию ниже 👇", reply_markup=main_menu)


@router.message(F.text == "Мои услуги")
async def my_services(msg: types.Message):
    sent = await send_services(msg)
    if not sent:
        await msg.answer("Пока нет услуг")
    await msg.answer("Нажмите 'Назад' для возврата", reply_markup=back_kb)


@router.message(F.text == "Назад")
async def back_to_menu(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Главное меню", reply_markup=main_menu)

@router.message(F.text == "Заполнить анкету")
async def fill_form(msg: types.Message, state: FSMContext):
    await state.set_state(RequestForm.service)
    await msg.answer("Какая из моих услуг Вам интересна? (Например: рилс, генерация, автоматизация, логотип и т.п", reply_markup=cancel_kb)

@router.message(RequestForm.service, F.text == "Отмена")
@router.message(RequestForm.description, F.text == "Отмена")
@router.message(RequestForm.contact, F.text == "Отмена")
async def cancel_form(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Действие отменено", reply_markup=main_menu)

@router.message(RequestForm.service)
async def process_service(msg: types.Message, state: FSMContext):
    await state.update_data(service=msg.text)
    await state.set_state(RequestForm.description)
    await msg.answer(
        "Расскажите подробнее, для чего мы это делаем:\n— Добавьте ссылку на ваш бренд / магазин / соцсети \n— Кратко опишите задачу \n— При желании прикрепите референсы, скриншоты или любые другие материалы",
        reply_markup=cancel_kb
    )

@router.message(RequestForm.description)
async def process_description(msg: types.Message, state: FSMContext):
    text = msg.text or msg.caption or ""
    media = None
    if msg.photo:
        media = f"photo:{msg.photo[-1].file_id}"
    elif msg.video:
        media = f"video:{msg.video.file_id}"
    await state.update_data(description=text, media=media)
    await state.set_state(RequestForm.contact)
    await msg.answer("Оставьте контактные данные для связи", reply_markup=cancel_kb)


@router.message(RequestForm.contact)
async def process_contact(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    service = data.get("service")
    description = data.get("description")
    media = data.get("media")
    contact = msg.text
    db.add_request(
        msg.from_user.id,
        msg.from_user.username or "",
        service,
        description,
        contact,
        media,
    )
    await state.clear()
    await msg.answer(
        "Спасибо большое за заявку! \U0001F64C\nМой ассистент проанализирует и передаст мне. Обязательно свяжусь с вами в ближайшее время.",
        reply_markup=main_menu
    )
    try:
        text = (
            f"Новая заявка #{msg.from_user.id}\n"
            f"Пользователь: {msg.from_user.username or msg.from_user.id}\n"
            f"Услуга: {service}\n"
            f"Описание: {description}\n"
            f"Контакты: {contact}"
        )
        if media:
            kind, file_id = media.split(":", 1)
            if kind == "photo":
                await msg.bot.send_photo(settings.admin_id, file_id, caption=text)
            else:
                await msg.bot.send_video(settings.admin_id, file_id, caption=text)
        else:
            await msg.bot.send_message(settings.admin_id, text)
    except Exception:
        pass

@router.message(F.text == "Написать напрямую DaniAi")
async def contact_direct(msg: types.Message):
    await msg.answer("Свяжитесь: @DaniAi_2")