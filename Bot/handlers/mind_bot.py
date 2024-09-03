from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from Bot.FSM.user_fsm import Photo
from Bot.kbds import reply as kb
from Bot.message.builder import StartMessage

from utils.db import DB

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

_BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=_BOT_TOKEN)
_USER_ROUTER = Router()
List_photo = {}

@_USER_ROUTER.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.answer("")
    temp_db = DB()
    person = temp_db.get_user(id_telegram=callback.message.chat.id)
    await callback.message.answer(StartMessage.old(person), parse_mode='html', reply_markup=kb.keyboard_start)

@_USER_ROUTER.callback_query(F.data == "save_photo")
@_USER_ROUTER.callback_query(F.data == "save_new_photo")
async def read_count_photo(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer("Укажите количество добавляемых фото: ")
    await state.set_state(Photo.Count)


@_USER_ROUTER.message(Photo.Count, F.text)
async def get_photo(message: Message, state: FSMContext):
    if int(message.text) > 10:
        await message.answer(
            text=f"⚠️Вы можете загрузить за раз не более 10 изображений.",
            reply_markup=kb.keyboard_start
        )
        await state.clear()
    else:
        await state.update_data(count=message.text)
        print(message.text)
        print(await state.get_data())
        await message.answer(
            text=f"Пришлите изображение(я) одним сообщением."
        )
        await state.set_state(Photo.photo_id)


@_USER_ROUTER.message(Photo.photo_id, F.photo)
async def get_photo(message: Message, state: FSMContext):
    temp_db = DB()

    global List_photo
    data = await state.get_data()
    key = str(message.from_user.id)
    List_photo.setdefault(key, [])
    if message.content_type == 'photo':
        List_photo[key].append(message.photo[-1].file_id)
        if len(List_photo[key]) == int(data["count"]):
            temp_db.add_user_list_photo(message.chat.id, List_photo[str(message.chat.id)])
            for item in List_photo[str(message.chat.id)]:
                file = await bot.get_file(item)
                file_path = file.file_path
                await bot.download_file(file_path, destination=f"static/image/{item}.jpg")
            await message.answer(
                text=
                "✅Изображение успешно сохранено!\n\n"
                f"Для доступа перейдите по ссылке/{List_photo[str(message.chat.id)][0]}",
                reply_markup=kb.keyboard_next)
            await state.clear()
            List_photo = {}

    temp_db.close_connect()


@_USER_ROUTER.message(Photo.photo_id, F.document)
async def get_photo(message: Message, state: FSMContext):
    temp_db = DB()

    global List_photo
    data = await state.get_data()
    key = str(message.from_user.id)
    List_photo.setdefault(key, [])
    if message.content_type == 'document':
        List_photo[key].append(message.document.file_id)
    if len(List_photo[key]) == int(data["count"]):
        temp_db.add_user_list_photo( message.chat.id, List_photo[str(message.chat.id)])
        for item in List_photo[str(message.chat.id)]:
            file = await bot.get_file(item)
            file_path = file.file_path
            await bot.download_file(file_path, destination=f"static/image/{item}.jpg")
        await message.answer(
            text=
            "✅Изображение успешно сохранено!\n\n"
            f"Для доступа перейдите по ссылке {List_photo[str(message.chat.id)][0]}",
            reply_markup=kb.keyboard_next)
        await state.clear()
        List_photo = {}

    temp_db.close_connect()