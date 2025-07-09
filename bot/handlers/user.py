from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.fsm.context import FSMContext
from ..keyboards.common import main_menu, cancel_kb, back_kb
from ..states.forms import RequestForm
from ..db.dao import Database
from ..config import settings

router = Router()

db = Database(settings.db_path)

@router.message(CommandStart())
async def start(msg: types.Message):
    db.add_user(msg.from_user.id, msg.from_user.username or "")
    text = (
        "\U0001F7E2 Стартовое сообщение:  Привет!  Я — DaniAi 2.0: создаю AI-визуал, стиль и Reels, собранные из нейросетей."\
        "  Ниже можешь посмотреть мои услуги и выбрать, как связаться \U0001F447"\
    )
    await msg.answer(text, reply_markup=main_menu)


@router.message(F.text == "Мои услуги")
async def my_services(msg: types.Message):
    services = db.get_services()
    if not services:
        await msg.answer("Пока нет услуг", reply_markup=back_kb)
        return
    text = "\n".join(f"• {s[1]}" for s in services)
    await msg.answer(text, reply_markup=back_kb)


@router.message(F.text == "Назад")
async def back_to_menu(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Главное меню", reply_markup=main_menu)

@router.message(F.text == "Заполнить анкету")
async def fill_form(msg: types.Message, state: FSMContext):
    await state.set_state(RequestForm.service)
    await msg.answer("Какую услугу вы хотите?", reply_markup=cancel_kb)

@router.message(RequestForm.service, F.text == "Отмена")
@router.message(RequestForm.description, F.text == "Отмена")
async def cancel_form(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Действие отменено", reply_markup=main_menu)

@router.message(RequestForm.service)
async def process_service(msg: types.Message, state: FSMContext):
    await state.update_data(service=msg.text)
    await state.set_state(RequestForm.description)
    await msg.answer(
        "Скиньте, для чего мы это делаем: — ссылка на ваш бренд / магазин / соцсети — описание задачи — референсы, скриншоты, любые медиа (по желанию)",
        reply_markup=cancel_kb
    )

@router.message(RequestForm.description)
async def process_description(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    service = data.get("service")
    description = msg.text
    db.add_request(msg.from_user.id, msg.from_user.username or "", service, description)
    await state.clear()
    await msg.answer(
        "Спасибо большое за заявку! \U0001F64C\nМой ассистент всё обработает и передаст мне. Я всё проанализирую и свяжусь с вами в ближайшее время.",
        reply_markup=main_menu
    )

@router.message(F.text == "Написать напрямую DaniAi")
async def contact_direct(msg: types.Message):
    await msg.answer("Свяжитесь: @DaniAi_2")
