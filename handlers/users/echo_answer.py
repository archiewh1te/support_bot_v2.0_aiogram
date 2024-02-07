from aiogram import types
from filters import IsPrivate_call
from keyboards.inline import kb_cancel_question, kb_regisration_user
from loader import dp
from state import send_app_from_user
from utils.db_api import register_commands as commands


# инлаин кнопка Задать вопрос из режима Эхо
@dp.callback_query_handler(IsPrivate_call(),text_contains='start_question')
async def send_answer(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    try:
        user = await commands.select_user(call.from_user.id)
        if user.status == 'active':
            await call.answer(cache_time=5)
            await call.message.answer(f"📝 Здравствуйте, формат заявки: Вы указываете магазин и номер кассы, ваша проблема с которой вы столкнулись (Можно и нужно прикрепить фото):", reply_markup=kb_cancel_question)
            await send_app_from_user.text.set()
        elif user.status == 'baned':
            await call.message.answer('⛔Вы забанены!⛔')
    except Exception:
        who = "@" + call.from_user.first_name
        await call.message.answer(f'Приветствую тебя {who}!\n'
                             f'Ты попал в <b>тех.поддержку</b> 🛠\n'
                             f'Для продолжения вам нужно зарегистрироваться, '
                             'нажмите клавишу 📝<b>Регистрация</b> или воспользуйтесь командой <b>/reg</b>', reply_markup=kb_regisration_user)
