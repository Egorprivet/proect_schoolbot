from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Главная клавиатура
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👨‍🏫 Учитель'), KeyboardButton(text='👦 Ученик')],
        [KeyboardButton(text='❓ Помощь')]
    ],
    resize_keyboard=True,
    persistent=True
)

# Клавиатура для учителя
teacher_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📋 Выбрать класс'), KeyboardButton(text='📅 Расписание всех классов')],
        [KeyboardButton(text='📝 ДЗ класса'), KeyboardButton(text='🔙 Главное меню')]
    ],
    resize_keyboard=True
)

# Клавиатура для ученика
student_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📊 Мои оценки'), KeyboardButton(text='📅 Расписание на завтра')],
        [KeyboardButton(text='📅 Расписание на неделю'), KeyboardButton(text='📝 ДЗ на завтра')],
        [KeyboardButton(text='🔙 Главное меню')]
    ],
    resize_keyboard=True
)

# Клавиатура классов для учителя
classes_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='5А'), KeyboardButton(text='5Б')],
        [KeyboardButton(text='6А'), KeyboardButton(text='6Б')],
        [KeyboardButton(text='🔙 Главное меню')]
    ],
    resize_keyboard=True
)

# Главное меню
main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👨‍🏫 Учитель'), KeyboardButton(text='👦 Ученик')],
        [KeyboardButton(text='🔙 Главное меню')]
    ],
    resize_keyboard=True
)
