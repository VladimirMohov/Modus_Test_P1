from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import html, Router, F, Bot
from utils.db import DB
from ..message.builder import StartMessage
from ..FSM.user_fsm import Photo
from aiogram.fsm.context import FSMContext
from ..kbds import reply as kb
from dotenv import load_dotenv, find_dotenv

from os import getenv

load_dotenv(find_dotenv())

bot = Bot(token=getenv('BOT_TOKEN'))
_USER_ROUTER = Router()
_ADMIN_ID = getenv("admin_id")

@_USER_ROUTER.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Отлов сообщения /start
    """
    temp_db = DB()
    person = temp_db.get_user(id_telegram=message.chat.id)
    print(_ADMIN_ID)
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

@_USER_ROUTER.callback_query(F.data == 'add')
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
