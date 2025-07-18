from aiogram import Router, types
from aiogram import F
from ..db.dao import Database
from ..config import settings
from ..keyboards.common import (
    admin_menu,
    main_menu,
    cancel_kb,
    back_kb,
    requests_kb,
    request_detail_kb,
    confirm_delete_kb,
    finish_services_kb,
)
from aiogram.fsm.context import FSMContext
from ..states.forms import ServicesMessageForm, NewsForm

router = Router()

db = Database(settings.db_path)


@router.message(ServicesMessageForm.content, F.text == "Отмена")
@router.message(NewsForm.content, F.text == "Отмена")
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


@router.callback_query(F.data == "admin_back")
async def admin_back_cb(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != settings.admin_id:
        await call.answer()
        return
    await state.clear()
    await call.message.delete()
    await call.message.answer("Админ меню", reply_markup=admin_menu)

@router.message(F.text == "Список заявок")
async def list_requests(msg: types.Message):
    if msg.from_user.id != settings.admin_id:
        return
    entries = db.get_requests()
    if not entries:
        await msg.answer("Заявок нет", reply_markup=admin_menu)
        return
    await msg.answer("Заявки:", reply_markup=requests_kb(entries))


@router.message(F.text == "Редактировать услуги")
async def edit_services(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    await state.set_state(ServicesMessageForm.content)
    await msg.answer(
        "Отправьте одно или несколько сообщений с описанием услуг.\n"
        "Когда закончите, нажмите 'Готово'.",
        reply_markup=finish_services_kb,
    )

@router.message(ServicesMessageForm.content, F.text == "Готово")
async def finalize_services(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    data = await state.get_data()
    messages = data.get("messages", [])
    db.save_service_messages(messages)
    await state.clear()
    await msg.answer("Сообщения сохранены", reply_markup=admin_menu)


@router.message(ServicesMessageForm.content)
async def collect_service_message(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(msg.message_id)
    await state.update_data(messages=messages)
    await msg.answer(
        "Добавлено. Пришлите еще или нажмите 'Готово'",
        reply_markup=finish_services_kb,
    )


@router.message(F.text == "Отправка рассылки")
async def start_news(msg: types.Message, state: FSMContext):
    if msg.from_user.id != settings.admin_id:
        return
    await state.set_state(NewsForm.content)
    await msg.answer("Отправьте сообщение для рассылки", reply_markup=cancel_kb)


@router.message(NewsForm.content)
async def send_news(msg: types.Message, state: FSMContext):
    users = db.get_users()
    for user_id, in users:
        try:
            await msg.bot.copy_message(user_id, msg.chat.id, msg.message_id)
        except Exception:
            pass
    await msg.answer("Отправлено. Можете прислать еще или отменить", reply_markup=cancel_kb)



@router.callback_query(F.data.startswith("req_"))
async def show_request(call: types.CallbackQuery):
    if call.from_user.id != settings.admin_id:
        await call.answer()
        return
    req_id = int(call.data.split("_", 1)[1])
    req = db.get_request(req_id)
    if not req:
        await call.message.edit_text("Заявка не найдена", reply_markup=admin_menu)
        return
    text = (
        f"Заявка #{req[0]}\n"
        f"User: {req[2]}\n"
        f"Service: {req[3]}\n"
        f"Desc: {req[4]}\n"
        f"Contact: {req[5]}"
    )
    media = req[6]
    await call.message.delete()
    if media:
        kind, file_id = media.split(":", 1)
        if kind == "photo":
            await call.message.answer_photo(file_id, caption=text, reply_markup=request_detail_kb(req_id))
        else:
            await call.message.answer_video(file_id, caption=text, reply_markup=request_detail_kb(req_id))
    else:
        await call.message.answer(text, reply_markup=request_detail_kb(req_id))


@router.callback_query(F.data.startswith("back_requests"))
async def back_requests(call: types.CallbackQuery):
    if call.from_user.id != settings.admin_id:
        await call.answer()
        return
    entries = db.get_requests()
    await call.message.delete()
    if not entries:
        await call.message.answer("Заявок нет", reply_markup=admin_menu)
        return
    await call.message.answer("Заявки:", reply_markup=requests_kb(entries))


@router.callback_query(F.data.startswith("del_"))
async def del_request_prompt(call: types.CallbackQuery):
    if call.from_user.id != settings.admin_id:
        await call.answer()
        return
    req_id = int(call.data.split("_", 1)[1])
    await call.message.edit_reply_markup(reply_markup=confirm_delete_kb(req_id))


@router.callback_query(F.data.startswith("delc_"))
async def del_request(call: types.CallbackQuery):
    if call.from_user.id != settings.admin_id:
        await call.answer()
        return
    req_id = int(call.data.split("_", 1)[1])
    db.delete_request(req_id)
    await call.message.delete()
    await call.message.answer("Заявка удалена", reply_markup=admin_menu)