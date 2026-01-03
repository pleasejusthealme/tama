import asyncio
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import register_handlers

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    register_handlers(dp)
    print("Бот запущен и ждет сообщений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())