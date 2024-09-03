from asyncio import run

from Bot.create_bot import bot, dp


async def main():

    # dp.update.middleware(getLastMessage())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        print('Bot ended')