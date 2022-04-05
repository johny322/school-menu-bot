from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, CommandStart

from data.config import MENU
from data.vote_results import VOTE_IDS
from keyboards.default.menu_keyboards import meals_types_markup, choose_meal_food, confirm_markup
from loader import dp
from aiogram import types

from utils.set_menu_from_file import async_add_vote_id, async_add_vote_values, async_get_vote_result


def create_text(meal_name: str, meal_num: int):
    menu_data = MENU[meal_name][meal_num]
    meal_type = list(menu_data.keys())[0]
    food_names = '\n'.join([f'{num}-{name}' for num, name in menu_data[meal_type].items()])
    text = f'Выбор {meal_type}:\n' \
           f'{food_names}\n' \
           f'Для выхода нажми кнопку Отмена'
    return text, len(menu_data[meal_type]), menu_data[meal_type], meal_type


@dp.message_handler(Text('отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Отмена', reply_markup=meals_types_markup)


@dp.message_handler(CommandStart())
async def choose_meal(message: types.Message, state: FSMContext):
    await state.finish()
    text = f'Привет, {message.from_user.first_name}\n' \
           f'Выбери прием пищи'
    await message.answer(text, reply_markup=meals_types_markup)


@dp.message_handler(lambda message: not message.text.isdigit(), state='test_state')
async def wrong_input(message: types.Message, state: FSMContext):
    await message.answer('Неверный формат')


@dp.message_handler(lambda message: message.text.isdigit(), state='test_state')
@dp.message_handler(text=['Завтрак', 'Обед', 'Ужин', 'Полдник'])
async def get_food(message: types.Message, state: FSMContext):
    await state.set_state('test_state')
    data = await state.get_data()
    prev_num = data.get('prev_num')
    name = data.get('name')
    if name is not None:
        meal_name = name
    else:
        meal_name = message.text.lower()

    if message.from_user.id in VOTE_IDS[meal_name]:
        await message.answer('Твой голос уже был учтен')
        await state.finish()
        return
    if prev_num is None:
        text, length, menu_data, meal_type = create_text(meal_name, 0)
        await message.answer(text, reply_markup=choose_meal_food(length))
        async with state.proxy() as data:
            data['name'] = meal_name
            data['answers'] = {}
            data['length'] = length
            data['prev_num'] = 0
    else:
        max_length = len(MENU[meal_name])
        _, old_length, old_meal_data, old_meal_type = create_text(meal_name, prev_num)
        if message.text.isdigit():
            if int(message.text) not in range(1, old_length + 1):
                await message.answer('Неверный формат')
                return
        if prev_num == max_length - 1:
            async with state.proxy() as data:
                data['answers'][old_meal_type] = old_meal_data[message.text]
            await confirm_choose(message, state)
        else:
            text, length, menu_data, meal_type = create_text(meal_name, prev_num + 1)
            await message.answer(text, reply_markup=choose_meal_food(length))
            async with state.proxy() as data:
                data['answers'][old_meal_type] = old_meal_data[message.text]
                data['length'] = length
                data['prev_num'] = prev_num + 1


@dp.message_handler(state='confirm_state', text='Нет')
async def cancel_choose_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    meal_name = data.get('name')
    await state.reset_state(with_data=True)
    async with state.proxy() as data:
        data['name'] = meal_name
    await get_food(message, state)


@dp.message_handler(state='confirm_state', text='Да')
async def confirm_choose_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    await message.answer(f'Твой выбор на {data["name"]} будет учтен', reply_markup=meals_types_markup)
    await async_add_vote_id(data["name"], message.from_user.id)
    await async_add_vote_values(data)
    text = await async_get_vote_result()
    await message.answer(text)


async def confirm_choose(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = f'Ты выбрал:\n' + '\n'.join([f'{meal_type}-{name}' for meal_type, name in data['answers'].items()]) + \
               '\nПодтвердить выбор?'
    await message.answer(text, reply_markup=confirm_markup)
    await state.set_state('confirm_state')
