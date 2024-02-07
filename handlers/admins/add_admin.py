from aiogram import types
from loader import dp, bot
from filters import IsPrivate
from utils.db_api import admins_commands as commands
from utils.misc import rate_limit
from data.config import cfg

teh_chat_id = cfg['teh_chat_id']


# Регистрация админов
@rate_limit(limit=3)
@dp.message_handler(IsPrivate(), text='/newadmin')
async def admins_add(message: types.Message):
    who = "@" + message.from_user.get_mention(as_html=True)
    try:
        admin = await commands.select_admin(message.from_user.id)
        if admin.flag == 'admin':
            await message.answer(f'Привет {who}! \n'
                                 f'Вы попали в раздел администраторов\n'
                                 f'<code>/clist</code> - <b>Список доступных команд</b>\n')

    except Exception:
        await commands.add_admins(user_id=message.from_user.id,
                                  first_name=message.from_user.first_name,
                                  last_name=message.from_user.last_name,
                                  user_name=message.from_user.username,
                                  status='active',
                                  flag='noadmin',
                                  access=int(0))
        await message.answer('Вы теперь добавлены как сотрудник техподдержки, ожидайте свои права Администратора')
        await bot.send_message(teh_chat_id, f"У нас новый сотрудник Тех.Поддержки\n"
                                            f"<b>Ник:</b>  {who} \n"
                                            f"<b>Айди:</b> {message.from_user.id}")
