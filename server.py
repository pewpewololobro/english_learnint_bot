from bot import bot, dp
from aiogram.utils import executor
from aiogram import types
from model import User, Word, Translate, WordTranslate
import re, json
import peewee
from random import shuffle

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
async def get_test(message : types.Message, user = None):
	user = user or User.get(external_id = message.from_user.id, chat_id = message.chat.id)
	pairs = WordTranslate.select()\
	.where(WordTranslate.user == user)\
	.order_by(peewee.fn.Random())\
	.limit(4)
	markup = types.InlineKeyboardMarkup()
	buttons = []
	question = None
	for row in pairs:
		word = Word.get(Word.id == row.word.id, Word.user == row.user)
		translate = Translate.get(Translate.id == row.translate.id, Translate.user == row.user)
		if question is None:
			question = word
		btn = types.InlineKeyboardButton(
			text = f'{row.translate.translate}',
			callback_data = json.dumps(
				{'t' : 'a', 'q' : question.id, 'a' : translate.id}
			)
		)
		buttons.append(btn)
	shuffle(buttons)
	markup.add(*buttons[:2])
	markup.add(*buttons[2:])
	await bot.send_message(user.chat_id, f"Слово {question.word}", reply_markup = markup)

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)