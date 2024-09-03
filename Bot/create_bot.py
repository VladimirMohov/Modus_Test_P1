from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
import os

_BOT_TOKEN = os.getenv("BOT_TOKEN")
_REDIS_HOST = os.getenv("redis_host") 
_REDIS_PORT = os.getenv("redis_port")
_REDIS_DB = os.getenv("redis_db")
_REDIS_PASSWORD = os.getenv("redis_password")

storage = RedisStorage(
    host=_REDIS_HOST, 
    port=_REDIS_PORT,
    db=_REDIS_DB,
    password=_REDIS_PASSWORD,
)

bot = Bot(token=_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
