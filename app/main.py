import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from bot import dp  # Импортируем dp из файла bot.py
from settings import settings  # Импортируем settings из файла settings.py

# Добавляем функцию приветствия
@dp.message(F.text == "/start")
async def welcome(message: Message, bot: Bot) -> None:
    await message.answer("Добро пожаловать! Я бот для скачивания TikTok видео. Отправьте мне ссылку на видео TikTok.")

async def start() -> None:
    bot = Bot(token=settings.api_token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())
