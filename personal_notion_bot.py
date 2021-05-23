import logging
from pathlib import Path
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

path = Path('/home/parax/Telegram_bot/personal-notion-bot/bot_token.txt')
API_TOKEN = path.read_text().strip()
logging.basicConfig(level=logging.INFO)
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

Dict = {"chosen_name":"","content":""}

class Waiting(StatesGroup):
    waiting_for_name = State()
    waiting_for_content = State()

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['help']) #ф-я выводящая help
async def send_help(message: types.Message):
	await message.answer('Пока тут пусто')


@dp.message_handler(commands=['new_page'])
async def new_page(message: types.Message, state: FSMContext):
	await message.answer('Введите название')
	await Waiting.waiting_for_name.set()

@dp.message_handler(state = Waiting.waiting_for_name, content_types=types.ContentTypes.TEXT)
async def name_chosen(message: types.Message, state: FSMContext):
	await state.update_data(chosen_name = message.text.lower())
	await message.answer("Теперь прикрепите контент")
	await Waiting.next()

@dp.message_handler(state = Waiting.waiting_for_content, content_types=types.ContentTypes.TEXT)
async def content(message: types.Message, state: FSMContext):
	await state.update_data(content = message.text.lower())
	await state.finish()

if __name__ == '__main__':
   	executor.start_polling(dp, skip_updates=True)