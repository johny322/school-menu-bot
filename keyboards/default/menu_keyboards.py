from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

meals_types_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Завтрак')
        ],
        [
            KeyboardButton(text='Обед')
        ],
        [
            KeyboardButton(text='Ужин')
        ],
        [
            KeyboardButton(text='Полдник')
        ]

    ],
    resize_keyboard=True
)

admin_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Посмотреть меню'), KeyboardButton(text='Изменить меню и сбросить результаты')
        ],
        [
            KeyboardButton(text='Результаты голосования'), KeyboardButton(text='Сбросить результаты голосования')
        ]
    ],
    resize_keyboard=True
)

cancel_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)

confirm_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'), KeyboardButton(text='Нет')
        ]
    ],
    resize_keyboard=True
)


# def choose_meal_food(meal_data: dict):
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[[KeyboardButton(text=str(i))] for i in range(1, len(meal_data) + 1)],
#         resize_keyboard=True
#     )
#     return keyboard

def choose_meal_food(length: int):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=str(i))] for i in range(1, length + 1)] + [[KeyboardButton(text='Отмена')]],
        resize_keyboard=True
    )
    return keyboard
