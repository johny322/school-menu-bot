import json

from data.config import MENU
from data.vote_results import RESULTS, VOTE_IDS
from utils.async_wraps import run_blocking_io


def set_menu():
    with open('data/menu.json', encoding='utf-8') as f:
        menu = json.load(f)
    for key in menu:
        MENU[key] = menu[key]
    # print(MENU)
    set_vote_ids()
    set_results()


async def async_set_menu():
    return await run_blocking_io(set_menu)


def set_vote_ids():
    # print(VOTE_IDS)
    for key in MENU:
        VOTE_IDS[key] = []
    # print(VOTE_IDS)


async def async_set_vote_ids():
    return await run_blocking_io(set_vote_ids)


def add_vote_id(meal_name, id):
    if meal_name in VOTE_IDS:
        VOTE_IDS[meal_name].append(id)


async def async_add_vote_id(meal_name, id):
    await run_blocking_io(add_vote_id, meal_name, id)


def add_vote_values(data: dict):
    meal_name = data['name']
    for num, meal_data in enumerate(data['answers'].items()):
        meal_type, food_name = meal_data
        RESULTS[meal_name][num][meal_type][food_name] += 1


async def async_add_vote_values(data: dict):
    await run_blocking_io(add_vote_values, data)


def get_menu():
    try:
        with open('data/menu.json', encoding='utf-8') as f:
            menu: dict = json.load(f)
    except FileNotFoundError:
        return
    text = ''
    for key, values in menu.items():
        text += f"<b>{key}</b>\n"
        food_text = ''
        for value in values:
            meal_type = list(value.keys())[0]
            food_text += f"<i>{meal_type}</i>\n"
            menu_data = value[meal_type]
            food_names = '\n'.join([f'{num}-{name}' for num, name in menu_data.items()])
            food_text += food_names + '\n\n'
        text += food_text
    return text


async def async_get_menu():
    return await run_blocking_io(get_menu)


def set_results():
    for meal_names, meal_datas in MENU.items():
        RESULTS[meal_names] = []
        for meal_data in meal_datas:
            meal_type = list(meal_data.keys())[0]

            food_names = list(meal_data[meal_type].values())
            RESULTS[meal_names].append({
                meal_type: dict.fromkeys(food_names, 0)
            })
    # pprint(RESULTS)


async def async_set_results():
    await run_blocking_io(set_results)


def get_vote_result():
    text = '<b>РЕЗУЛЬТАТЫ</b>\n'
    for key, values in RESULTS.items():
        text += f"<b>{key}</b>\n"
        food_text = ''
        for value in values:
            meal_type = list(value.keys())[0]
            food_text += f"<i>{meal_type}</i>\n"
            menu_data = value[meal_type]

            sorted_tuples = sorted(menu_data.items(), key=lambda item: item[1], reverse=True)
            sorted_menu_data = {k: v for k, v in sorted_tuples}

            food_names = '\n'.join([f'{name}: {vote_value}' for name, vote_value in sorted_menu_data.items()])
            food_text += food_names + '\n\n'
        text += food_text
    return text


async def async_get_vote_result():
    return await run_blocking_io(get_vote_result)
