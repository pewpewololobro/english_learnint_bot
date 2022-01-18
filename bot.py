from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
import os


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

async def on_startup(_):
	print('Bot started')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)