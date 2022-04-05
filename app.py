from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.set_menu_from_file import async_set_menu, async_set_results, async_set_vote_ids


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    await async_set_menu()
    await async_set_vote_ids()
    await async_set_results()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

