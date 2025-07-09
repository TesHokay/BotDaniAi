from aiogram import Router, types
from aiogram import F
from ..db.dao import Database
from ..config import settings
from ..keyboards.common import admin_menu, main_menu, cancel_kb, back_kb
from aiogram.fsm.context import FSMContext
from ..states.forms import ExampleForm, ServiceForm, NewsForm

router = Router()

db = Database(settings.db_path)


@router.message(ExampleForm.file, F.text == "Отмена")
@router.message(ExampleForm.caption, F.text == "Отмена")
@router.message(ServiceForm.name, F.text == "Отмена")
@router.message(NewsForm.text, F.text == "Отмена")
async def cancel_state(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    await state.clear()
    await msg.answer("Действие отменено", reply_markup=admin_menu)

@router.message(F.text == "admin")
async def admin_start(msg: types.Message):
    if msg.from_user.id != settings.admin_id:
        return
    await msg.answer("Админ меню", reply_markup=admin_menu)


@router.message(F.text == "Назад")
async def admin_back(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    await state.clear()
    await msg.answer("Главное меню", reply_markup=main_menu)

@router.message(F.text == "Список заявок")
async def list_requests(msg: types.Message):
    if msg.from_user.id != settings.admin_id:
        return
    entries = db.get_requests()
    if not entries:
        await msg.answer("Заявок нет", reply_markup=admin_menu)
        return
    text = "\n".join(f"#{e[0]} | {e[2]} | {e[3]}\n{e[4]}" for e in entries)
    await msg.answer(text, reply_markup=admin_menu)


@router.message(F.text == "Добавить услугу")
async def add_service(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    await state.set_state(ServiceForm.name)
    await msg.answer("Название услуги", reply_markup=cancel_kb)


@router.message(ServiceForm.name)
async def service_name(msg: types.Message, state: FSMContext):
    db.add_service(msg.text)
    await state.clear()
    await msg.answer("Услуга добавлена", reply_markup=admin_menu)


@router.message(F.text == "Рассылка новости")
async def start_news(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    await state.set_state(NewsForm.text)
    await msg.answer("Введите текст рассылки", reply_markup=cancel_kb)


@router.message(NewsForm.text)
async def send_news(msg: types.Message, state: FSMContext):
    users = db.get_users()
    for user_id, in users:
        try:
            await msg.bot.send_message(user_id, msg.text)
        except Exception:
            pass
    await state.clear()
    await msg.answer("Рассылка завершена", reply_markup=admin_menu)

@router.message(F.text == "Добавить пример работы")
async def add_example(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    await state.set_state(ExampleForm.file)
    await msg.answer("Отправьте картинку или видео", reply_markup=cancel_kb)


@router.message(ExampleForm.file, F.photo | F.video)
async def example_file(msg: types.Message, state: FSMContext):
    file_id = msg.photo[-1].file_id if msg.photo else msg.video.file_id
    await state.update_data(file_id=file_id)
    await state.set_state(ExampleForm.caption)
    await msg.answer("Добавьте подпись", reply_markup=cancel_kb)


@router.message(ExampleForm.caption, F.text)
async def example_caption(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    db.add_example(data["file_id"], msg.text)
    await state.clear()
    await msg.answer("Пример добавлен", reply_markup=admin_menu)
