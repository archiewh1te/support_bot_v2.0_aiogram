from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsPrivate, IsAdminCheck
from state.admin_notice import FSM_Notice_admin
from loader import dp, bot
import logging
from data.config import admins


@dp.message_handler(IsPrivate(), IsAdminCheck(), commands=['нотис', 'notice'])
async def notice_admin(message: types.Message):
    await message.answer(f"✏Введите текст для отправки уведомления тех.поддержке:")
    await FSM_Notice_admin.text.set()



# Обработчики
@dp.message_handler(state=FSM_Notice_admin.text, content_types=['photo', 'text'])
async def send_notice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if (message.content_type == 'photo'):
            data['text'] = message.caption
        else:
            data['text'] = message.text
    await state.finish()
    if (message.chat.username == None):
        who = "Ник не установлен"
    else:
        who = "@" + message.from_user.first_name
    question = data['text']

    if (message.content_type == 'photo'):
        ph = message.photo[0].file_id
        await message.reply(f"✉ Ваше уведомление для Тех Поддержки было отослано.")
        await bot.send_photo(ph, caption=f"✉ | ❗️❗️❗️Новое уведомление для Тех Поддержки❗️❗️❗️\nОт: {message.from_user.first_name}\n"
                                                        f"Текст: ⚠️<code>{data['text']}</code>⚠️\n\n")

    else:
        await message.reply(f"✉ Ваше уведомление для Тех Поддержки было отослано.")
        for admin in admins:
            try:
                text = (f"✉ | ❗️❗️❗️Новое уведомление для Тех Поддержки❗️❗️❗️\nОт: {message.from_user.first_name}\n"
                                                        f"Текст: ⚠️<b>{data['text']}</b>⚠️\n\n")
                await bot.send_message(chat_id=admin, text=text)
            except Exception as err:
                logging.exception(err)
