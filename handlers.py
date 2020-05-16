import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text, CommandStart
from keyboards import rps_menu
from state import Game
import database
import sticker_id
from load_all import bot, dp

db = database.DBCommands()


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    user = await db.add_new_user()
    if user[1] == 'old':
        text = f'Вы уже зарегистрированы'
        await bot.send_message(chat_id, text)
    else:
        text = f'Приветствую вас, {user[0].full_name}'
        await bot.send_message(chat_id, text)


@dp.message_handler(commands=['hw'])
async def my_hw(message: types.Message):
    chat_id = message.from_user.id
    homework_list = list(db.list_unmade_hw())
    for homework in homework_list:
        text = homework.title
        await bot.send_message(chat_id, text)
