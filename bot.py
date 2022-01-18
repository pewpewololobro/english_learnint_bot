from aiogram import Bot, types, Dispatcher
import os


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
	print('Bot started')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)