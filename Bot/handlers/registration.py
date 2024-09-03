from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from utils.db import DB
from Bot.message.builder import StartMessage
from Bot.kbds import reply as kb
from dotenv import load_dotenv, find_dotenv

from os import getenv

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

_BOT_TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
_USER_REGISTRY_ROUTER = Router()
_ADMIN_ID = getenv("admin_id")

@_USER_REGISTRY_ROUTER.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отлов сообщения /start
    """
    temp_db = DB()
    person = temp_db.get_user(id_telegram=message.chat.id)
    # Пользователь существует.
    if person is not None:
        await message.answer(StartMessage.old(person), parse_mode='html', reply_markup=kb.keyboard_start)
    else:
        await message.answer("Ваша заявка находится на проверке. Пожалуйста ожидайте.😊")
        await bot.send_message(chat_id=_ADMIN_ID, text=f'Новый пользователь!\n'
                                                   f'ID:{message.from_user.id}\n'
                                                   f'username: @{message.from_user.username}\n',
                               reply_markup=kb.add_user)
        
    temp_db.close_connect()

@_USER_REGISTRY_ROUTER.callback_query(F.data == 'add')
async def add_user(cb: CallbackQuery):
    await cb.answer('')
    message = cb.message.text
    username_pos = message.find('username')
    user_id = message[message.find('ID') + 3:username_pos - 1]

    obj = {
        'id': user_id,
        'user_name': message[username_pos + 11:],
    }

    temp_db = DB()

    temp_db.add_user(obj['id'], obj['user_name'])
    person = temp_db.get_user(id_telegram=obj['id'])
    await bot.send_message(chat_id=user_id, text=StartMessage.old(person), parse_mode='html',
                           reply_markup=kb.keyboard_start)
