import asyncio
import os
from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command
from dotenv import find_dotenv, load_dotenv
from kbds import start_kb, teacher_kb, student_kb, classes_kb, main_menu_kb

load_dotenv(find_dotenv())
user_private_router = Router()

# Состояния пользователей
user_roles = {}  # {user_id: 'teacher' или 'student'}
selected_class = {}  # {user_id: '5А'}


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("👋 Привет! Это виртуальный помощник школы!\n\nВыберите кем будете:", reply_markup=start_kb)


# Выбор роли
@user_private_router.message(F.text == "👨‍🏫 Учитель")
async def choose_teacher(message: types.Message):
    user_id = message.from_user.id
    user_roles[user_id] = 'teacher'
    await message.answer("✅ Вы выбрали роль Учителя!\n\nЧто хотите сделать?", reply_markup=teacher_kb)


@user_private_router.message(F.text == "👦 Ученик")
async def choose_student(message: types.Message):
    user_id = message.from_user.id
    user_roles[user_id] = 'student'
    await message.answer("✅ Вы выбрали роль Ученика!\n\nЧто хотите посмотреть?", reply_markup=student_kb)


# === УЧИТЕЛЬСКИЕ ФУНКЦИИ ===
@user_private_router.message(F.text == "📋 Выбрать класс")
async def select_class(message: types.Message):
    user_id = message.from_user.id
    if user_roles.get(user_id) != 'teacher':
        await message.answer("❌ Доступно только учителям!", reply_markup=main_menu_kb)
        return
    await message.answer("📋 Выберите класс:", reply_markup=classes_kb)


@user_private_router.message(F.text.in_({"5А", "5Б", "6А", "6Б"}))
async def class_selected(message: types.Message):
    user_id = message.from_user.id
    if user_roles.get(user_id) != 'teacher':
        await message.answer("❌ Доступно только учителям!", reply_markup=main_menu_kb)
        return

    selected_class[user_id] = message.text
    class_data = {
        "5А": {"Иванов": 4.5, "Петров": 4.2, "Сидоров": 5.0},
        "5Б": {"Козлов": 4.8, "Смирнов": 3.9, "Попов": 4.7},
        "6А": {"Васильев": 4.3, "Морозов": 4.6, "Новиков": 4.9},
        "6Б": {"Федоров": 4.1, "Михайлов": 4.4, "Кузнецов": 5.0}
    }

    grades = class_data.get(message.text, {})
    text = f"📊 **Класс {message.text}**\n\n"
    for student, grade in grades.items():
        text += f"• {student}: {grade}\n"

    await message.answer(text, parse_mode="Markdown")
    await message.answer("Что дальше?", reply_markup=teacher_kb)


@user_private_router.message(F.text == "📅 Расписание всех классов")
async def all_schedules(message: types.Message):
    if user_roles.get(message.from_user.id) != 'teacher':
        await message.answer("❌ Доступно только учителям!", reply_markup=main_menu_kb)
        return

    text = """
📅 **РАСПИСАНИЕ ВСЕХ КЛАССОВ**

**5А, 5Б:**
Пн: Математика, Русский, Физика
Вт: История, Биология, Литература

**6А, 6Б:**
Пн: Алгебра, География, Английский
Вт: Физика, Обществознание, Музыка
    """
    await message.answer(text, parse_mode="Markdown")


@user_private_router.message(F.text == "📝 ДЗ класса")
async def homework_input(message: types.Message):
    user_id = message.from_user.id
    if user_roles.get(user_id) != 'teacher':
        await message.answer("❌ Доступно только учителям!", reply_markup=main_menu_kb)
        return

    current_class = selected_class.get(user_id, "5А")
    await message.answer(
        f"📝 **Введите ДЗ для класса {current_class}:**\n\n"
        f"Пример: Математика - стр.15 №3-7, Русский - сочинение 150 слов",
        parse_mode="Markdown"
    )


# === УЧЕНИЧЕСКИЕ ФУНКЦИИ ===
@user_private_router.message(F.text == "📊 Мои оценки")
@user_private_router.message(Command('evaluations'))
async def student_grades(message: types.Message):
    if user_roles.get(message.from_user.id) != 'student':
        await message.answer("❌ Доступно только ученикам!", reply_markup=main_menu_kb)
        return

    text = """
📊 **ВАШИ ОЦЕНКИ:**

Математика: 4, 5, 3
Русский: 4, 4, 5
Физика: 5, 4
Английский: 5, 5
Средний балл: 4.5
    """
    await message.answer(text, parse_mode="Markdown")


@user_private_router.message(F.text == "📅 Расписание на завтра")
@user_private_router.message(Command('lessons'))
async def tomorrow_schedule(message: types.Message):
    if user_roles.get(message.from_user.id) != 'student':
        await message.answer("❌ Доступно только ученикам!", reply_markup=main_menu_kb)
        return

    text = """
📅 **ЗАВТРА (Понедельник):**

8:00 - Математика
9:40 - Русский язык
11:20 - Физика
13:40 - Английский
15:20 - История
    """
    await message.answer(text, parse_mode="Markdown")


@user_private_router.message(F.text == "📅 Расписание на неделю")
async def week_schedule(message: types.Message):
    if user_roles.get(message.from_user.id) != 'student':
        await message.answer("❌ Доступно только ученикам!", reply_markup=main_menu_kb)
        return

    text = """
📅 **РАСПИСАНИЕ НА НЕДЕЛЮ:**

**Пн:** Математика | Русский | Физика
**Вт:** История | Биология | Литература  
**Ср:** Алгебра | География | Английский
**Чт:** Физика | Обществознание | Музыка
**Пт:** Технология | Физра | физра
    """
    await message.answer(text, parse_mode="Markdown")


@user_private_router.message(F.text == "📝 ДЗ на завтра")
async def tomorrow_homework(message: types.Message):
    if user_roles.get(message.from_user.id) != 'student':
        await message.answer("❌ Доступно только ученикам!", reply_markup=main_menu_kb)
        return

    text = """
📝 **ДОМАШНЕЕ ЗАДАНИЕ НА ЗАВТРА:**

• Математика: стр.15 №3-7
• Русский: сочинение 150 слов  
• Физика: параграф 2.1, вопросы
• Английский: выучить слова (20 шт.)
    """
    await message.answer(text, parse_mode="Markdown")


# Общие команды
@user_private_router.message(F.text == "🔙 Главное меню")
async def back_to_main(message: types.Message):
    await message.answer("🏠 Главное меню:", reply_markup=start_kb)


@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('🤖 Вкратце что умеет бот:\n• Просмотр оценок\n• Расписание\n• ДЗ\n• Функции для учителей')


@user_private_router.message(F.text.in_(["❓ Помощь", "/help"]))
async def help_cmd(message: types.Message):
    await message.answer('🆘 Если нужна помощь, обращайтесь по номеру: +7 (343) 123-45-67')
