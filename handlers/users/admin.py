from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from filters.admin_filter import IsAdmin
from keyboards.default.menu_keyboards import admin_markup, cancel_markup
from loader import dp
from aiogram import types

from utils.set_menu_from_file import async_get_menu, async_set_menu, async_set_results, async_get_vote_result, \
    async_set_vote_ids


@dp.message_handler(IsAdmin(), Text('отмена', ignore_case=True), state='new_menu')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Отмена', reply_markup=admin_markup)


@dp.message_handler(IsAdmin(), Command('admin'))
async def admin_handler(message: types.Message):
    await message.answer('Повар', reply_markup=admin_markup)


@dp.message_handler(IsAdmin(), text='Сбросить результаты голосования')
async def reset_vote_results_handler(message: types.Message, state: FSMContext):
    await async_set_results()
    await async_set_vote_ids()
    await message.answer('Результаты голосования сброшены')


@dp.message_handler(text='Результаты голосования')
async def get_vote_results_handler(message: types.Message, state: FSMContext):
    res = await async_get_vote_result()
    await message.answer(res)


@dp.message_handler(IsAdmin(), state='new_menu', content_types=types.ContentType.DOCUMENT)
async def set_menu_handler(message: types.Message, state: FSMContext):
    file = message.document
    if not file.file_name.lower().endswith('.json'):
        await message.answer('Неверный формат файла')
        return
    await file.download(destination_file='data/menu.json')
    try:
        await async_set_menu()
        await message.answer('Меню обновлено', reply_markup=admin_markup)
    except Exception:
        await message.answer('Не удалось обновить меню', reply_markup=admin_markup)
    await state.finish()


@dp.message_handler(IsAdmin(), text='Изменить меню и сбросить результаты')
async def get_menu_handler(message: types.Message, state: FSMContext):
    await message.answer('Отправьте файл json с меню', reply_markup=cancel_markup)
    await state.set_state('new_menu')


@dp.message_handler(IsAdmin(), text='Посмотреть меню')
async def get_menu_handler(message: types.Message, state: FSMContext):
    text = await async_get_menu()
    await message.answer(text)
