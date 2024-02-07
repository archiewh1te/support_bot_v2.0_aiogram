import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

# Для уведомлений о запуске бота В ЛС
admins = [
    123456789, 123456789, 123456789
]

cfg = {

    'dev_id': 123456789,  # ID Разработчика
    'teh_chat_id': -123456789,  # ID админской группы


    # УРОВНИ ДОСТУПА
    '1lvl_adm_name': 'Тех.поддержка',
    '2lvl_adm_name': 'Администратор',
    '3lvl_adm_name': 'Руководитель'
}

ip = os.getenv('ip')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}'
