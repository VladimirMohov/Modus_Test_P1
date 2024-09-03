from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from .handlers.registration import _USER_ROUTER
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

_BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_routers(_USER_ROUTER)