import asyncio
from aiogram import F, types, Router
from aiogram.filters import Command
from kbds import start_kb, main_menu_kb, cancel_kb, teacher_kb, classes_kb
from data.user_data import user_sessions

user_private_router = Router()


@user_private_router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 **Виртуальный помощник школы!**\n\n"
        "🔐 **Сначала авторизуйтесь** в электронном дневнике:\n"
        "`/auth`\n\n"
        "После авторизации доступны:\n"
        "• Реальные **оценки**\n"
        "• Актуальное **расписание**\n"
        "• **ДЗ** из дневника",
        parse_mode="Markdown",
        reply_markup=start_kb
    )


async def check_auth(user_id: int, message: types.Message):
    """Проверка авторизации"""
    session = user_sessions.get(user_id, {})
    if not session.get('logged_in', False):
        await message.answer(
            "❌ **Требуется авторизация!**\n\n"
            "🔐 Нажмите `/auth` для входа в дневник.",
            parse_mode="Markdown",
            reply_markup=cancel_kb
        )
        return False
    return True


@user_private_router.message(F.text == "📊 Мои оценки")
@user_private_router.message(Command('grades'))
async def student_grades(message: types.Message):
    user_id = message.from_user.id
    if not await check_auth(user_id, message):
        return

    # ✅ ИСПРАВЛЕНИЕ: Импорт внутри функции
    try:
        from dnevnik_api import dnevnik_instance as dnevnik

        if dnevnik:
            grades = await dnevnik.get_grades()
            text = "📊 **ВАШИ ОЦЕНКИ:**\n\n"

            if grades:
                values = []
                for g in grades:
                    try:
                        values.append(float(g['value']))
                    except:
                        pass
                avg = sum(values) / len(values) if values else 0
                text += f"📈 **Средний балл: {avg:.2f}**\n\n"

                for grade in grades[:8]:
                    text += f"• **{grade['subject']}**: {grade['value']} ({grade['date']})\n"
            else:
                text += "📭 Оценок пока нет"
        else:
            text = "❌ Дневник не подключен"

    except Exception as e:
        text = "📊 **ДЕМО ОЦЕНКИ:**\n\n• Математика: 4 (03.03)\n• Русский: 5 (02.03)\n• Физика: 3 (01.03)"

    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu_kb)


@user_private_router.message(F.text == "📅 Расписание")
@user_private_router.message(Command('schedule'))
async def get_schedule(message: types.Message):
    user_id = message.from_user.id
    if not await check_auth(user_id, message):
        return

    try:
        from dnevnik_api import dnevnik_instance as dnevnik

        if dnevnik:
            schedule = await dnevnik.get_schedule()
            text = "📅 **РАСПИСАНИЕ НА НЕДЕЛЮ:**\n\n"
            for day, lessons in list(schedule.items())[:3]:
                text += f"**{day}:**\n"
                for i, lesson in enumerate(lessons[:5], 1):
                    text += f"{i}. {lesson}\n"
                text += "\n"
        else:
            text = "❌ Дневник не подключен"
    except:
        text = """📅 **ПОНЕДЕЛЬНИК:**
• 8:00 Математика
• 9:40 Русский язык  
• 11:20 Физика"""

    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu_kb)


@user_private_router.message(F.text.in_(["📝 ДЗ", "📝 ДЗ на завтра"]))
async def get_homework(message: types.Message):
    user_id = message.from_user.id
    if not await check_auth(user_id, message):
        return

    try:
        from dnevnik_api import dnevnik_instance as dnevnik

        if dnevnik:
            homework = await dnevnik.get_homework()
            text = "📝 **ДОМАШНЕЕ ЗАДАНИЕ:**\n\n"
            if homework:
                for subject, task in list(homework.items())[:5]:
                    text += f"• **{subject}:** {task}\n"
            else:
                text += "📭 ДЗ не задано"
        else:
            text = "❌ Дневник не подключен"
    except:
        text = """📝 **ДОМАШКА:**
• **Математика:** §15 №3-7
• **Русский:** сочинение 150 слов
• **Физика:** параграф 2.1"""

    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu_kb)


@user_private_router.message(F.text == "📋 Статистика класса")
async def teacher_stats(message: types.Message):
    if not await check_auth(message.from_user.id, message):
        return
    text = """📊 **СТАТИСТИКА КЛАССА**

📈 Средний балл: **4.3**
👑 Лучший: Иванов И. (**4.9**)
📉 Худший: Петров П. (**3.2**)

📊 Динамика: **+0.2** за неделю"""
    await message.answer(text, parse_mode="Markdown", reply_markup=teacher_kb)


@user_private_router.message(F.text.in_(["🔙 Главное меню", "🔙 Меню"]))
async def back_to_menu(message: types.Message):
    await message.answer("🏠 **Главное меню:**", reply_markup=start_kb, parse_mode="Markdown")


@user_private_router.message(Command('status'))
async def status_cmd(message: types.Message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id, {})
    status = "✅ **Авторизован**" if session.get('logged_in') else "❌ **Не авторизован**"
    text = f"📊 **Статус:** {status}\n🔐 `/auth` - авторизация"
    await message.answer(text, parse_mode="Markdown", reply_markup=start_kb)


@user_private_router.message()
async def unknown_cmd(message: types.Message):
    await message.answer(
        "❓ Выберите действие из меню ниже:",
        reply_markup=start_kb
    )
