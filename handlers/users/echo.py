from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.group import IsGroup
from loader import dp


@dp.message_handler(IsGroup())
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer(f"Эхо: {message.text}\n")


# @dp.message_handler(state=None)
# async def bot_echo(message: types.Message, state: FSMContext):
#     await message.answer(f"Эхо: {message.text}\n"
#                          f"{message.from_user.url}\n"
#                          f"{message.contact}\n"
#                          # f"{message.url}\n"
#                          f"{message.from_user.username}")
