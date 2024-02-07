from aiogram import types
from keyboards.inline import kb_start_question, kb_regisration_user
from loader import dp, bot
from utils.misc import rate_limit
from utils.db_api import register_commands as commands
from filters import IsPrivate


# хендлер при команде /start или при нажатии кнопки Запустить бота
@rate_limit(limit=5)
@dp.message_handler(IsPrivate(), commands=['старт','start'])
async def client_start(message: types.Message):
    try:
       user = await commands.select_registration_by_user_id(message.from_user.id)
       if user.status == 'active':
           await message.answer(f'Приветствую тебя @<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>!\n'
                                f'✅Вы уже <b>зарегистрированы!</b>\n'
                                f'Вы попали в <b>тех.поддержку</b> 🛠\n'
                                f'Чтобы начать нажмите кнопку <b>✉Задать вопрос</b>\n'
                                , reply_markup=kb_start_question)
       elif user.status == 'baned':
           await message.answer('⛔Вы забанены!⛔')
    except Exception:
        await message.answer(f'Приветствую тебя @<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>!\n'
                             f'Вы попали в <b>тех.поддержку</b> 🛠\n'
                             f'Для продолжения вам нужно зарегистрироваться, '
                             'нажмите клавишу 📝<b>Регистрация</b> или воспользуйтесь командой <b>/reg</b>', reply_markup=kb_regisration_user)


# Команда просмотра профиля Юзера
@dp.message_handler(IsPrivate(), commands=['мойпрофиль','profiles'])
async def get_profile(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    if user.status == 'active':
        await message.answer(f'<code>Ваш 🆔</code> - <b>{user.user_id}</b>\n'
                         f'<code>👤Ваше Имя</code>: <b>{user.username}</b>\n'
                         f'<code>👤Ваша Фамилия</code>: <b>{user.famils}</b>\n'
                         f'<code>first_name</code>: <b>{user.tg_first_name}</b>\n'
                         f'<code>last_name</code>: <b>{user.tg_last_name}</b>\n'
                         f'<code>🕵️‍Статус</code>: <b>{user.status}</b>\n'
                         f'<code>📞Телефон</code>: <b>{user.phone}</b>\n'
                         f'<code>🏢Магазин</code>: <b>{user.magazin}</b>\n')
    elif user.status == 'baned':
        await message.answer('⛔Вы забанены!⛔')


