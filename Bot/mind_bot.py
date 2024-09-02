from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html
from create_bot import bot, dp

import asyncio

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отлов сообщения /start
    """
    await message.answer("Hello, {}!".format(html.bold(message.from_user.full_name)))

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Отлов всех сообщений
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())