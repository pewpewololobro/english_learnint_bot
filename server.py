from bot import bot, dp
from aiogram.utils import executor
from aiogram import types
from model import User, Word, Translate, WordTranslate
import re
import peewee

pattern = re.compile(r'/add[\s]([\w]+)[\s]([\w]+)')

@dp.message_handler(commands = ['start'])
async def on_startup(message : types.Message):
	await message.answer(message.text)

@dp.message_handler(commands = ['add'])
async def add_word(message : types.Message):
	user, __ = User.get_or_create(external_id = message.from_user.id, chat_id = message.chat.id)
	txt = message.text
	word_and_translate = pattern.match(txt)
	raw_word, raw_translate = tuple(i.lower() for i in word_and_translate.groups())
	word, __ = Word.get_or_create(word = raw_word, user = user)
	translate, __ = Translate.get_or_create(translate = raw_translate, user = user)
	WordTranslate.get_or_create(word = word, translate = translate, user = user)
	await message.answer(f'Добавлео слово "{raw_word}" с переводом "{raw_translate}"')

@dp.message_handler(commands = ['test'])
async def get_test(message, user = None):
	user = user or User.get(external_id = message.from_user.id, chat_id = message.chat.id)
	pairs = WordTranslate.select()\
	.where(WordTranslate.user == user)\
	.order_by(peewee.fn.Radom())\
	.limit(4)
	

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)