import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

from handlers.user_private import user_private_router
from handlers.auth import auth_router  # ← ДОБАВИТЬ
from common.bot_cmds_list import private

ALLOWED_UPDATES = ['message', 'edited_message']

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=os.getenv('TOKEN'))

dp.include_router(auth_router)
dp.include_router(user_private_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    print("🚀 Бот запущен!")
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == "__main__":
    asyncio.run(main())
