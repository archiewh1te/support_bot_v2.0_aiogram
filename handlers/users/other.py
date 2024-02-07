from aiogram import types
from filters import IsPrivate
from keyboards.inline.start_question import kb_start_question
from loader import dp


# пустой хендлер отвечает на все сообщения к боту
@dp.message_handler(IsPrivate())
async def send_message(message: types.Message):
    await message.reply(f'Бот <b>не видит 👀</b> что вы пишите, если вы подали заявку то дождитесь ответа от Технической поддержки.\n'
                            f'Если ответа нет, то начните сначала,\n'
                            f'нажмите кнопку <b>✉Задать вопрос</b>\n'
                            f'❗Просьба <b>закрывать заявки</b> после ответа от Технической поддержки❗', reply_markup=kb_start_question)





