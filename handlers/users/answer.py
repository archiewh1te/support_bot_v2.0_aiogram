import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import cfg
from filters import IsPrivate_call, IsPrivate
from handlers.users.buttons import tehchatid
from keyboards.inline import kb_start_question
from loader import dp, bot
from state import send_app_from_user
from utils.db_api import register_commands as commands, admins_commands

devid = cfg['dev_id']
teh_chat_id = cfg['teh_chat_id']


# При нажатии на кнопку Заявка закрыта
# @dp.callback_query_handler(IsPrivate_call(), text_contains='app_closed')
# async def app_closed(call: types.CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=5)
#     reply_msg = await call.message.reply(f'Вы успешно <b>закрыли</b> заявку. 👍')
#     await call.message.answer(f'Чтобы задать вопрос сначала,\n'
#                               f'нажмите кнопку <b>✉ Задать вопрос</b>', reply_markup=kb_start_question)
#     user = await commands.select_user(call.from_user.id)
#     await bot.send_message(teh_chat_id, f'✅ Заявка от <b>{user.famils} {user.username}</b> из Организации <b>{user.magazin}</b> успешно закрыта!')
#     await state.finish()
#     await asyncio.sleep(5)
#     await call.message.delete()
#     await reply_msg.delete()


# # При нажатии на кнопку Заявка не закрыта
# @dp.callback_query_handler(text_contains='app_open')
# async def app_open(call: types.CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=5)
#     await call.message.delete()
#     await state.finish()
#     await call.message.answer('Продолжите диалог с тех.поддержкой: ')
#     await send_app_from_user.text.set()
#     user = await commands.select_user(call.from_user.id)
#     await bot.send_message(teh_chat_id, f'💬Пользователь <b>{user.famils} {user.username}</b> из Организации <b>{user.magazin}</b> не закрыл заявку, и продолжил диалог!')



