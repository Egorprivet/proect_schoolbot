import asyncio
from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from kbds import cancel_kb, main_menu_kb, start_kb
from data.user_data import user_sessions

auth_router = Router()


class AuthStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()


@auth_router.message(Command('auth'))
@auth_router.message(F.text.in_(["🔐 Авторизоваться в дневнике", "🔐 Авторизоваться", "🔐 Повторить авторизацию"]))
async def start_auth(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_sessions[user_id] = {'role': None, 'logged_in': False, 'login': '', 'password': ''}

    await message.answer(
        "📱 **Введите логин** от dnevnik.egov66.ru:\n\n"
        "*(номер телефона или email)*",
        parse_mode="Markdown",
        reply_markup=cancel_kb
    )
    await state.set_state(AuthStates.waiting_for_login)


@auth_router.message(AuthStates.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    login = message.text.strip()

    if login.lower() in ['отмена', '❌ отмена', '❌']:
        await message.answer("❌ Авторизация отменена.", reply_markup=start_kb)
        await state.clear()
        return

    user_sessions[user_id]['login'] = login
    await message.answer(
        f"✅ Логин сохранен: `{login}`\n\n"
        "🔑 **Введите пароль**:",
        parse_mode="Markdown",
        reply_markup=cancel_kb
    )
    await state.set_state(AuthStates.waiting_for_password)


@auth_router.message(AuthStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    password = message.text.strip()

    if password.lower() in ['отмена', '❌ отмена', '❌']:
        await message.answer("❌ Авторизация отменена.", reply_markup=start_kb)
        await state.clear()
        return

    #  САХРАНЯЕМ Логин/Пароль
    session = user_sessions.setdefault(user_id, {})
    session['login'] = session.get('login', '')
    session['password'] = password

    await message.answer("🔄 **Подключаюсь к дневнику...**\n⏳ Проверка авторизации...",
                         parse_mode="Markdown", reply_markup=None)

    try:
        #  Импорт внутри функции
        from dnevnik_api import init_dnevnik, dnevnik_instance

        #  АВТОРИЗАЦИЯ
        success = await init_dnevnik(session['login'], password)

        #  САХРАНЯЕМ СТАТУС ПЕРЕД clear()!
        if success:
            session['logged_in'] = True

            await message.answer(
                f"✅ **УСПЕШНАЯ АВТОРИЗАЦИЯ!**\n\n"
                f"👤 **Логин:** `{session['login']}`\n"
                f"📚 **Класс:** 5А\n\n"
                f"✨ **Теперь доступны:**\n"
                f"📊 Оценки | 📅 Расписание | 📝 ДЗ\n\n"
                f"📱 **Выберите действие:**",
                parse_mode="Markdown",
                reply_markup=main_menu_kb
            )
        else:
            await message.answer(
                "❌ **Ошибка авторизации!**\n\n"
                "🔍 **Попробуйте:**\n"
                "• Проверить логин/пароль\n"
                "• `/auth` еще раз\n\n"
                "**Повторите:** `/auth`",
                parse_mode="Markdown",
                reply_markup=cancel_kb
            )

    except Exception as e:
        await message.answer(
            f"❌ **Ошибка:** `{str(e)[:80]}`\n\n"
            "**Начните заново:** `/auth`",
            parse_mode="Markdown",
            reply_markup=cancel_kb
        )

    #  clear() в самом конце
    await state.clear()
