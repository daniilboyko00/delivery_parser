from distutils.cmd import Command
from imaplib import Commands
import logging
from aiogram import Bot, Dispatcher, executor, types
import os
import aiogram
from parser import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

R = os.environ.get('API_KEY')
bot = Bot(token=R)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
logging.basicConfig(filename='logs.txt',level=logging.ERROR)
my_command = ['csv', 'json', 'cancel']


class UserState(StatesGroup):
    waiting_for_number = State()
    format_choice = State()


@dp.message_handler(commands=['start'])
async def number_start(message: types.Message):
    await message.answer('Введите номер посылки')
    await UserState.waiting_for_number.set()


@dp.message_handler(state=UserState.waiting_for_number)
async def input_number(message: types.Message, state: FSMContext):
    await state.update_data(package_number = message.text.upper())
    data = await state.get_data()
    b = Parser(data['package_number'])
    if b.get_page_data():
        await message.answer('Введите /csv чтобы получить файл в формате csv, /json, чтобы в json формате')
        await UserState.format_choice.set()
        return b
    else: 
        await UserState.waiting_for_number.set()
        await message.answer('Информации по данному номеру не найдено или его не сущесвтует. Введите номер поссылки еще раз')

    
@dp.message_handler(commands=my_command, state=UserState.format_choice)
async def get_csv(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    if message.text == '/csv':
        b.create_csv()
        file_csv = aiogram.types.input_file.InputFile('app/output_files/data.csv','data.csv')
        await Bot.send_document(bot,chat_id=user_id,document=file_csv)
        await message.answer(f"Путь поссылки №{data['package_number']} в формате csv. Введите /json чтобы получить json, либо /cancel чтобы заново ввести номер")
        await UserState.format_choice.set()
    elif message.text == '/json':
        b.create_json()
        file_json = aiogram.types.input_file.InputFile('app/output_files/data.json','data.json')
        await Bot.send_document(bot,chat_id=user_id,document=file_json)
        await message.answer(f"Путь поссылки №{data['package_number']} в формате json. Введите /csv чтобы получить csv, либо /cancel чтобы заново ввести номер")
        await UserState.format_choice.set()
    elif message.text == '/cancel':
        await UserState.waiting_for_number.set()
        await message.answer('Введите номер поссылки')

    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
