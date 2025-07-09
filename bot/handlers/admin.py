from aiogram import Router, types
from aiogram import F
from ..db.dao import Database
from ..config import settings
from ..keyboards.common import admin_menu, main_menu

router = Router()

db = Database(settings.db_path)

@router.message(F.text == "admin")
async def admin_start(msg: types.Message):
    if msg.from_user.id != settings.admin_id:
        return
    await msg.answer("Админ меню", reply_markup=admin_menu)

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

@router.message(F.text == "Добавить пример работы")
async def add_example(msg: types.Message):
    if msg.from_user.id != settings.admin_id:
        return
    await msg.answer("Отправьте картинку или видео, которое хотите добавить в highlights")
