async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    from loader import db
    from utils.db_api.db_gino import on_startup
    print('Подключение к PostgreSQL')
    await on_startup(dp)

    # print('Удаление базы данных') # Команда на очистку БД при старте бота
    # await db.gino.drop_all()

    print('Создание таблиц')  # Команда на создание таблиц в БД
    await db.gino.create_all()

    import filters
    filters.setup(dp)

    from utils.notify_admins import on_startup_notify  # Импортируем функцию которая отправляет сообщения админам
    await on_startup_notify(dp)  # Запускаем функцию!

    from utils.set_bot_commands import set_default_commands  # Импортируем функцию которая устанавливает команды
    await set_default_commands(dp)  # Запускаем функцию!

    print('Бот запущен!')  # Вывод в консоль Бот запущен


if __name__ == '__main__':
    from aiogram import executor  # Импортируем executor для запуска полинга
    from handlers import dp  # Из хендлеров импортируем dp

    executor.start_polling(dp, on_startup=on_startup)  # Запускаем полинг бота, и функцию on_startup
