from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Клавиатуры для бота
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔐 Авторизоваться в дневнике")],

    ], 
    resize_keyboard=True,
    one_time_keyboard=False
)

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Мои оценки"), KeyboardButton(text="📅 Расписание")],
        [KeyboardButton(text="📝 ДЗ на завтра"), KeyboardButton(text="🔐 Повторить авторизацию")],
        [KeyboardButton(text="🔙 Главное меню")]
    ], 
    resize_keyboard=True
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Отмена")]
    ], 
    resize_keyboard=True,
    one_time_keyboard=True
)

teacher_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Статистика класса"), KeyboardButton(text="📅 Расписание всех классов")],
        [KeyboardButton(text="📝 ДЗ класса"), KeyboardButton(text="🔐 Повторить авторизацию")],
        [KeyboardButton(text="🔙 Главное меню")]
    ], 
    resize_keyboard=True
)

classes_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="8А"), KeyboardButton(text="8Б")],
        [KeyboardButton(text="7А"), KeyboardButton(text="10Б")],
        [KeyboardButton(text="❌ Отмена")]
    ], 
    resize_keyboard=True
)

